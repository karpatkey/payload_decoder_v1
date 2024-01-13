from defyes.functions import get_abi_function_signatures, get_contract, get_contract_proxy_abi, get_node, search_proxy_impl_address
from karpatkit.constants import Address, Chain
from defyes.explorer import ChainExplorer
import requests
import json
from pathlib import Path
import os
from dune_client.client import DuneClient
from dune_client.query import QueryBase

ROLES_ABI = '[{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_avatar","type":"address"},{"internalType":"address","name":"_target","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ArraysDifferentLength","type":"error"},{"inputs":[],"name":"ModuleTransactionFailed","type":"error"},{"inputs":[],"name":"NoMembership","type":"error"},{"inputs":[],"name":"SetUpModulesAlreadyCalled","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16[]","name":"roles","type":"uint16[]"},{"indexed":false,"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"AssignRoles","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousAvatar","type":"address"},{"indexed":true,"internalType":"address","name":"newAvatar","type":"address"}],"name":"AvatarSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"guard","type":"address"}],"name":"ChangedGuard","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"DisabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"EnabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"initiator","type":"address"},{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"avatar","type":"address"},{"indexed":false,"internalType":"address","name":"target","type":"address"}],"name":"RolesModSetup","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16","name":"defaultRole","type":"uint16"}],"name":"SetDefaultRole","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"multisendAddress","type":"address"}],"name":"SetMultisendAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousTarget","type":"address"},{"indexed":true,"internalType":"address","name":"newTarget","type":"address"}],"name":"TargetSet","type":"event"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"allowTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16[]","name":"_roles","type":"uint16[]"},{"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"assignRoles","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"avatar","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"defaultRoles","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prevModule","type":"address"},{"internalType":"address","name":"module","type":"address"}],"name":"disableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"}],"name":"enableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModule","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModuleReturnData","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRole","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRoleReturnData","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"returnData","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGuard","outputs":[{"internalType":"address","name":"_guard","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"start","type":"address"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getModulesPaginated","outputs":[{"internalType":"address[]","name":"array","type":"address[]"},{"internalType":"address","name":"next","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"guard","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_module","type":"address"}],"name":"isModuleEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"multisend","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"revokeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeAllowFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"bool[]","name":"isParamScoped","type":"bool[]"},{"internalType":"enum ParameterType[]","name":"paramType","type":"uint8[]"},{"internalType":"enum Comparison[]","name":"paramComp","type":"uint8[]"},{"internalType":"bytes[]","name":"compValue","type":"bytes[]"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunctionExecutionOptions","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"enum Comparison","name":"paramComp","type":"uint8"},{"internalType":"bytes","name":"compValue","type":"bytes"}],"name":"scopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"bytes[]","name":"compValues","type":"bytes[]"}],"name":"scopeParameterAsOneOf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"}],"name":"scopeRevokeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"scopeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_avatar","type":"address"}],"name":"setAvatar","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16","name":"role","type":"uint16"}],"name":"setDefaultRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_guard","type":"address"}],"name":"setGuard","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_multisend","type":"address"}],"name":"setMultisend","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_target","type":"address"}],"name":"setTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"initParams","type":"bytes"}],"name":"setUp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"target","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint8","name":"paramIndex","type":"uint8"}],"name":"unscopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
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
ExecutionOptions = {
    0: 'None',
    1: 'Send',
    2: 'DelegateCall',
    3: 'Both'
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

    if proxy_impl_address != Address.ZERO and blockchain == Chain.ETHEREUM:
        contract = get_contract_proxy_abi(contract_address, proxy_impl_address, blockchain, web3=web3)
    else:
        contract = get_contract(contract_address, blockchain, abi=ROLES_ABI)

    func_obj, func_params = contract.decode_function_input(data)

    func_sig = requests.get("https://api.openchain.xyz/signature-database/v1/lookup?function=%s&filter=true" % data[:10]).json()['result']['function'][data[:10]][0]['name']
    if func_sig == None:
        func_sig = requests.get("https://www.4byte.directory/api/v1/signatures/?hex_signature=%s" % data[:10]).json()['results'][0]['text_signature']
    
    components_names = [func_param for func_param in func_params]
    
    func_desc = get_function_description(func_sig, components_names)

    for func_param in func_params:
        if isinstance(func_params[func_param], bytes):
            func_params[func_param] = '0x' + func_params[func_param].hex()
            if func_param == 'functionSig':
                selector = func_params[func_param]
                selector_names = requests.get("https://api.openchain.xyz/signature-database/v1/lookup?function=%s&filter=true" % selector).json()['result']['function'][selector]
                if selector_names == None:
                    selector_names = requests.get("https://www.4byte.directory/api/v1/signatures/?hex_signature=%s" % selector).json()['results']
                
                # If the contract does not have the function, it checks if there is a proxy implementation
                proxy_impl_address = search_proxy_impl_address(func_params['targetAddress'], blockchain, web3=web3)

                if proxy_impl_address != Address.ZERO:
                    try:
                        target_contract = get_contract_proxy_abi(func_params['targetAddress'], proxy_impl_address, blockchain, web3=web3)
                    except Exception as e:
                        if (type(e) == ValueError and e.args[0] == 'ABI not verified.'):
                            break
                else:
                    try:
                        target_contract = get_contract(func_params['targetAddress'], blockchain)
                    except Exception as e:
                        if (type(e) == ValueError and e.args[0] == 'ABI not verified.'):
                            break
                
                signature = ''
                for selector_name in selector_names:
                    try:
                        getattr(target_contract.functions, selector_name['name'][:selector_name['name'].index('(')])
                        signature = selector_name['name']
                        break
                    except:
                        try:
                          getattr(target_contract.functions, selector_name['text_signature'][:selector_name['text_signature'].index('(')])
                          signature = selector_name['text_signature']
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
            elif func_param == 'options':
                func_params[func_param] = str(func_params[func_param]) + ': ' + ExecutionOptions[func_params[func_param]]
    
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
        'functionSelector': web3.keccak(text=func_sig).hex()[:10],
        'params': params,
    }

    return entry
