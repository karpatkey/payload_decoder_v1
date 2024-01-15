from karpatkit.constants import Chain
from utils.helper_functions import bcolors, decode_data, json_file_download, dune_query
import json
from tqdm import tqdm


print(f"{bcolors.HEADER}{bcolors.BOLD}-----------------------{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}--- Payload Decoder ---{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}-----------------------{bcolors.ENDC}")
print()

attributes_dict = Chain.__dict__
chain_dict = {
    key: value
    for key, value in Chain.__dict__.items()
    if (key[0].isupper() and key not in ['ROPSTEN', 'KOVAN', 'GOERLI'])
}

print(f"{bcolors.OKGREEN}{bcolors.BOLD}Select the blockchain: {bcolors.ENDC}")
index = 1
for chain in chain_dict:
    print(f"{bcolors.OKBLUE}{bcolors.BOLD}{index}- {chain}{bcolors.ENDC}")
    index += 1

chain_index = input(f"{bcolors.OKGREEN}{bcolors.BOLD}\nEnter your option: {bcolors.ENDC}")
n_chains = [str(x) for x in range(1, index)]
while chain_index not in n_chains:
    chain_index = int(input('Enter a valid option: '))

chain_list = list(chain_dict.items())
key = chain_list[int(chain_index) - 1][0]
blockchain = chain_dict[key]

path = input(f"{bcolors.OKGREEN}{bcolors.BOLD}\n\nEnter the path to the payload: {bcolors.ENDC}")

result = []

with open(path, 'r') as payload_file:
    # Reading from json file
    payload_data = json.load(payload_file)

dune_labels = dune_query()

id = 1
for txn in tqdm(payload_data['transactions']):
    result.append(decode_data(txn['to'], txn['data'], blockchain, id, dune_labels))
    id += 1

print()

if result != []:
    json_file_download(result)