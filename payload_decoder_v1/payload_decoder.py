from defyes.constants import Chain
from utils.helper_functions import bcolors, decode_data, json_file_download, dune_query
import json
from tqdm import tqdm


print(f"{bcolors.HEADER}{bcolors.BOLD}-----------------------{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}--- Payload Decoder ---{bcolors.ENDC}")
print(f"{bcolors.HEADER}{bcolors.BOLD}-----------------------{bcolors.ENDC}")
print()

path = input(f"{bcolors.OKGREEN}{bcolors.BOLD}Enter the path to the payload: {bcolors.ENDC}")

result = []

with open(path, 'r') as payload_file:
    # Reading from json file
    payload_data = json.load(payload_file)

dune_labels = dune_query()

id = 1
for txn in tqdm(payload_data['transactions']):
    result.append(decode_data(txn['to'], txn['data'], Chain.ETHEREUM, id, dune_labels))
    id += 1

print()

if result != []:
    json_file_download(result)