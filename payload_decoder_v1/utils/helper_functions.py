from defyes.functions import get_abi_function_signatures, get_contract, get_contract_proxy_abi, get_node, search_proxy_impl_address
from defyes.constants import Address
from defyes.explorer import ChainExplorer
import requests
import json
from pathlib import Path
import os
from dune_client.client import DuneClient
from dune_client.query import QueryBase


LABELS_FILE = Path(__file__).parent / "labels.json"
DUNE_LABELS_FILE = Path(__file__).parent / "dune_labels.json"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ParameterType = {
    0: 'Static',
    1: 'Dynamic',
    2: 'Dynamic32'
}
Comparison = {
    0: 'EqualTo',
    1: 'GreaterThan',
    2: 'LessThan',
    3: 'OneOf'
}


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# json_file_download
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def json_file_download(json_file):

    print(f"{bcolors.OKBLUE}-------------------------{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}--- JSON File Download---{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}-------------------------{bcolors.ENDC}")
    print()

    file_name = input('Enter the name of the JSON file: ')
    file_path = str(Path(os.path.abspath(__file__)).resolve().parents[1])+'/%s.json' % file_name
    print()
    try:
        with open(file_path, 'w') as file:
            json.dump(json_file, file, indent=4)
        
        message = 'JSON file %s was succesfully downloaded to the path: %s' % ('%s.json' % file_name, file_path)
        print(f"{bcolors.OKGREEN}{message}{bcolors.ENDC}")
    except Exception as e:
        message = 'ERROR: JSON file %s download fail' % ('%s.json' % file_name)
        print(f"{bcolors.FAIL}{message}{bcolors.ENDC}")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_function_description
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_function_description(function_signature, components_names):
    parts = function_signature.split(",")

    func_desc = ''
    if len(parts) == 1:
        if len(components_names) == 1:
            part = parts[0]
            index = part.find(')')
            func_desc += f"{part[:index]} {components_names[0]}{part[index:]}"
        else:
            func_desc = function_signature
    else:    
        for i, part in enumerate(parts):
            if part.find(')') == -1:
                func_desc += part + f" {components_names[i]}"
            else:
                index = part.find(')')
                func_desc += f"{part[:index]} {components_names[i]}{part[index:]}"
            
            if i < len(parts) - 1:
                func_desc += ", "
    
    return func_desc

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_api_keys_from_config
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_api_keys_from_config():
    config_path = os.environ.get("DECODER_CONFIG_PATH")

    if config_path and Path(config_path).exists():
        config_file = Path(config_path)
    else:
        current_dir = Path(__file__).resolve().parent
        config_file = current_dir / "config.json"

    with open(config_file) as json_file:
        config = json.load(json_file)
    
    return config["apikeys"]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# dune_query():
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dune_query():
    dune_labels = {}

    query = QueryBase(
    name="ZRM - ETH - Identifier Labels (API)",
    query_id=3173156)

    config_api_keys = get_api_keys_from_config()

    try:
        results = DuneClient(config_api_keys["dune"]).run_query(query)
        for row in results.result.rows:
            dune_labels[row['address'].lower()] = row['name']
        
        with open(DUNE_LABELS_FILE, 'w') as dune_labels_file:
            json.dump(dune_labels, dune_labels_file, indent=4)
    except:
        with open(DUNE_LABELS_FILE, 'r') as dune_labels_file:
            dune_labels = json.load(dune_labels_file)

    return dune_labels

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# decode_data
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def decode_data(contract_address, data, blockchain, id, dune_labels):
    web3 = get_node(blockchain)
    
    # If the contract does not have the function, it checks if there is a proxy implementation
    proxy_impl_address = search_proxy_impl_address(contract_address, blockchain, web3=web3)

    if proxy_impl_address != Address.ZERO:
        contract = get_contract_proxy_abi(contract_address, proxy_impl_address, blockchain, web3=web3)
    else:
        contract = get_contract(contract_address, blockchain)

    func_obj, func_params = contract.decode_function_input(data)

    func_sig = requests.get("https://api.openchain.xyz/signature-database/v1/lookup?function=%s&filter=true" % data[:10]).json()['result']['function'][data[:10]][0]['name']
    components_names = [func_param for func_param in func_params]
    
    func_desc = get_function_description(func_sig, components_names)

    for func_param in func_params:
        if isinstance(func_params[func_param], bytes):
            func_params[func_param] = '0x' + func_params[func_param].hex()
            if func_param == 'functionSig':
                selector = func_params[func_param]
                selector_names = requests.get("https://api.openchain.xyz/signature-database/v1/lookup?function=%s&filter=true" % selector).json()['result']['function'][selector]
                
                # If the contract does not have the function, it checks if there is a proxy implementation
                proxy_impl_address = search_proxy_impl_address(func_params['targetAddress'], blockchain, web3=web3)

                if proxy_impl_address != Address.ZERO:
                    target_contract = get_contract_proxy_abi(func_params['targetAddress'], proxy_impl_address, blockchain, web3=web3)
                else:
                    target_contract = get_contract(func_params['targetAddress'], blockchain)
                
                signature = ''
                for selector_name in selector_names:
                    try:
                        getattr(target_contract.functions, selector_name['name'][:selector_name['name'].index('(')])
                        signature = selector_name['name']
                        break
                    except:
                        continue
                
                if signature == '':
                    # Special cases where the function is not in the proxy nor in the implementation. 
                    # Example: Compound v3 Comets function allow(address,bool) which is in the cUSDCv3 Ext contract.
                    try:
                        proxy_impl_address = target_contract.functions.extensionDelegate().call()
                        target_contract = get_contract_proxy_abi(func_params['targetAddress'], proxy_impl_address, blockchain, web3=web3)
                        for selector_name in selector_names:
                            try:
                                getattr(target_contract.functions, selector_name['name'][:selector_name['name'].index('(')])
                                signature = selector_name['name']
                                break
                            except:
                                continue
                    except:
                            continue

                description = ''
                if signature != '':
                    # A function can have multiple version with the same name but different amount of parameters.
                    if proxy_impl_address != Address.ZERO:
                        matching_functions = get_abi_function_signatures(func_params['targetAddress'], blockchain, abi_address=proxy_impl_address, func_names=[signature[:signature.index('(')]])
                    else:
                        matching_functions = get_abi_function_signatures(func_params['targetAddress'], blockchain, func_names=[signature[:signature.index('(')]])
                    
                    for matching_function in matching_functions:
                        if matching_function['signature'] == signature:
                            break
                    description = get_function_description(signature, matching_function['components_names'])
                else:
                    signature = 'Unknown'
                    description = 'Unknown'

                func_params['functionSig'] = {
                    'selector': selector,
                    'signature': signature,
                    'description': description
                }

        elif isinstance(func_params[func_param], tuple) or isinstance(func_params[func_param], list):
            func_params[func_param] = list(func_params[func_param])
            for i in range(len(func_params[func_param])):
                if func_param == 'paramType':
                    func_params[func_param][i] = str(func_params[func_param][i]) + ': ' + ParameterType[func_params[func_param][i]]
                elif func_param == 'paramComp':
                    func_params[func_param][i] = str(func_params[func_param][i]) + ': ' + Comparison[func_params[func_param][i]]
                if isinstance(func_params[func_param][i], bytes):
                    func_params[func_param][i] = '0x' + func_params[func_param][i].hex()
        
        else:
            if func_param == 'paramType':
                func_params[func_param] = str(func_params[func_param]) + ': ' + ParameterType[func_params[func_param]]
    
    try:
        contract_name = contract.functions.symbol().call()
    except:
        contract_name = ChainExplorer(blockchain).get_contract_name(contract_address)

    params = {}
    for func_param in func_params:
        params[func_param] = func_params[func_param]
        if web3.is_address(func_params[func_param]):
            try:
                params[func_param+'Name'] = dune_labels[str(func_params[func_param]).lower()]
            except:
                params[func_param+'Name'] = 'Unknown'

    entry = {
        'id': id,
        'targetAddress': contract_address,
        'contractName': contract_name,
        'functionSignature': func_sig,
        'functionDescription': func_desc,
        'params': params,
    }

    return entry
