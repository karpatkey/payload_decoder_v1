# Payload Decoder v1

​
Payload Decoder v1 is a Python library designed to decode payloads for [Roles Modifier v1](https://github.com/gnosis/zodiac-modifier-roles-v1), developed by [Gnosis Guild](https://www.gnosisguild.org/).


## Zodiac Roles Modifier

​
The Roles Modifier belongs to the [Zodiac](https://github.com/gnosis/zodiac) collection of tools, which can be accessed through the Zodiac App available on [Gnosis Safe](https://gnosis-safe.io/), as well as in the Zodiac repository.
​<br>

If you have any questions about Zodiac, join the [Gnosis Guild Discord](https://discord.gg/wwmBWTgyEq). Follow [@GnosisGuild](https://twitter.com/gnosisguild) on Twitter for updates.


### About the Roles Modifier

​
This modifier allows avatars to enforce granular, role-based, permissions for attached modules.
​<br>

Modules that have been granted a role are able to unilaterally make calls to any approved addresses, approved functions, and approved variables the role has access to.
​<br>

The interface mirrors the relevant parts of the Gnosis Safe's interface, so this contract can be placed between Gnosis Safe modules and a Gnosis Safe to enforce role-based permissions.


### Entities

​
Thanks to [p2p.org](https://p2p.org/) for the entities concept.​

- **Zodiac Roles Modifier (Roles)** is contract developed by Gnosis Guild for non-custodial asset management. `Zodiac` is the name of the toolset. `Roles` is the name of the top-level contract. `Modifier` is a base contract for a subset of Zodiac tools, including Roles.
- **Avatar** (in Zodiac jargon) is an address that can be “piloted” meaning a certain action (contract call) can be made on its behalf by Pilot via Roles.
- **Pilot** (in Zodiac jargon) is an address approved by Avatar to do a certain action on its behalf via Roles.


## Roles.sol

​
Contains the functions that are exposed to being called by an Ethereum account. For creating/modifying/eliminating permissions granted to the Pilot account, `scoping` functions are called in the Roles contract deployed by the Avatar Safe (and can only be called by the owner).
​<br>

This functions, their parameters and their execution consequences can be found in the [Roles Modifier v1](https://github.com/gnosis/zodiac-modifier-roles-v1) repo and in each of the contract deployments made by Avatar's implementing the standard.
<br>

The main `scoping` functions called in any payload are described next (along with an example output in JSON format).


### `scopeTarget`


To interact with contracts they have to be scoped first (the contract address).
<br>

`scopeTarget` scopes calls to an address, limited to specific function signatures, and per function scoping rules.


```solidity
function scopeTarget(
    uint16 role, /// Role to set for
    address targetAddress /// Address to be scoped
)
```

```json
{
    "id": 80,
    "targetAddress": "0xf20325cf84b72e8BBF8D8984B8f0059B984B390B",
    "contractName": "Roles",
    "functionSignature": "scopeTarget(uint16,address)",
    "functionDescription": "scopeTarget(uint16 role, address targetAddress)",
    "functionSelector": "0x5e826695",
    "params": {
        "role": 1,
        "targetAddress": "0xBA12222222228d8Ba445958a75a0704d566BF2C8",
        "targetAddressName": "Balancer_v2: Vault"
    }
}
```


### `revokeTarget`

If no interactions are further needed with certain contracts they can be revoked, meaning the role no longer has permission interact with it.
<br>

`revokeTarget` disallows all calls made to an address


```solidity
function revokeTarget(
    uint16 role, /// Role to set for
    address targetAddress /// Address to be disallowed
)
```

```json
{
    "id": 30,
    "targetAddress": "0xf20325cf84b72e8BBF8D8984B8f0059B984B390B",
    "contractName": "Roles",
    "functionSignature": "revokeTarget(uint16,address)",
    "functionDescription": "revokeTarget(uint16 role, address targetAddress)",
    "functionSelector": "0x51fa1d73",
    "params": {
        "role": 1,
        "targetAddress": "0x59D66C58E83A26d6a0E35114323f65c3945c89c1",
        "targetAddressName": "Aura_finance: auraB_stETH_STABLE_REWARDER"
    }
}
```


### `scopeAllowFunction`


In order to call functions in scoped targets (contracts), functions have to be scoped.​
<br>

`scopeAllowFunction` allows a specific function signature on a scoped target (enables to call function from already scoped contract address in `scopeTarget` without any constraint).
​

```solidity
function scopeAllowFunction(
    uint16 role, /// Role to set for
    address targetAddress, /// Scoped address on which a function signature should be allowed
    bytes4 functionSig, /// Function signature to be allowed
    ExecutionOptions options /// Defines whether or not delegate calls and/or eth can be sent to the function
)
```

```json
{
    "id": 38,
    "targetAddress": "0xd8dd9164E765bEF903E429c9462E51F0Ea8514F9",
    "contractName": "Roles",
    "functionSignature": "scopeAllowFunction(uint16,address,bytes4,uint8)",
    "functionDescription": "scopeAllowFunction(uint16 role, address targetAddress, bytes4 functionSig, uint8 options)",
    "functionSelector": "0x2fcf52d1",
    "params": {
        "role": 1,
        "targetAddress": "0xDD3f50F8A6CafbE9b31a427582963f465E745AF8",
        "targetAddressName": "Rocketpool: RocketDepositPool",
        "functionSig": {
            "selector": "0xd0e30db0",
            "signature": "deposit()",
            "description": "deposit()"
        },
        "options": 1
    }
}
```


### `scopeRevokeFunction`

​
Similar to `revokeTarget`, if specific function calls are no longer needed they can be revoked, meaning the role no longer has permission to interact with it.​
<br>

`scopeRevokeFunction` disallows a specific function signature on a scoped target (disables the whitelisting of a scoped function).


```solidity
function scopeRevokeFunction(
    uint16 role, /// Role to set for
    address targetAddress, /// Scoped address on which a function signature should be disallowed
    bytes4 functionSig /// Function signature to be disallowed
)
```

```json
{
    "id": 31,
    "targetAddress": "0xf20325cf84b72e8BBF8D8984B8f0059B984B390B",
    "contractName": "Roles",
    "functionSignature": "scopeRevokeFunction(uint16,address,bytes4)",
    "functionDescription": "scopeRevokeFunction(uint16 role, address targetAddress, bytes4 functionSig)",
    "functionSelector": "0x2933ef1c",
    "params": {
        "role": 1,
        "targetAddress": "0x827179dD56d07A7eeA32e3873493835da2866976",
        "targetAddressName": "Sushi: RouteProcessor3",
        "functionSig": {
            "selector": "0x2646478b",
            "signature": "processRoute(address,uint256,address,uint256,address,bytes)",
            "description": "processRoute(address tokenIn, uint256 amountIn, address tokenOut, uint256 amountOutMin, address to, bytes route)"
        }
    }
}
```


### `scopeFunction`


Works the same way as `scopeAllowFunction`, but allows for constraining of call paramters only to single values.
<br>​

`scopeFunction` sets scoping rules for a function, on a scoped address.


```solidity
function scopeFunction(
    uint16 role, /// Role to set for
    address targetAddress, /// Scoped address on which scoping rules for a function are to be set
    bytes4 functionSig, /// Function signature to be scoped
    bool[] calldata isParamScoped, /// false for un-scoped, true for scoped
    ParameterType[] calldata paramType, /// Dynamic or Dynamic32, depending on the parameter type
    Comparison[] calldata paramComp, /// Any, or EqualTo, GreaterThan, or LessThan, depending on comparison type
    bytes[] memory compValue, /// The reference value used while comparing and authorizing
    ExecutionOptions options /// Defines whether or not delegate calls and/or eth can be sent to the function
)
```

```json
{
    "id": 24,
    "targetAddress": "0xd8dd9164E765bEF903E429c9462E51F0Ea8514F9",
    "contractName": "Roles",
    "functionSignature": "scopeFunction(uint16,address,bytes4,bool[],uint8[],uint8[],bytes[],uint8)",
    "functionDescription": "scopeFunction(uint16 role, address targetAddress, bytes4 functionSig, bool[] isParamScoped, uint8[] paramType, uint8[] paramComp, bytes[] compValue, uint8 options)",
    "functionSelector": "0x33a0480c",
    "params": {
        "role": 1,
        "targetAddress": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "targetAddressName": "Aave_v3: Pool",
        "functionSig": {
            "selector": "0x617ba037",
            "signature": "supply(address,uint256,address,uint16)",
            "description": "supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)"
        },
        "isParamScoped": [
            false,
            false,
            true
        ],
        "paramType": [
            "0: Static",
            "0: Static",
            "0: Static"
        ],
        "paramComp": [
            "0: EqualTo",
            "0: EqualTo",
            "0: EqualTo"
        ],
        "compValue": [
            "0x",
            "0x",
            "0x0000000000000000000000000efccbb9e2c09ea29551879bd9da32362b32fc89"
        ],
        "options": 0
    }
}
```


### `scopeParameterAsOneOf`


`scopeParameterAsOneOf` sets and enforces scoping rules, for a single parameter of a function, on a scoped target. (constraining the argument to be an element belonging in a given set). Parameter will be scoped with comparison type OneOf.


```solidity
function scopeParameterAsOneOf(
    uint16 role, /// Role to set for
    address targetAddress, /// Scoped address on which functionSig lives
    bytes4 functionSig, /// Function signature to be scoped
    uint256 paramIndex, /// The index of the parameter to scope
    ParameterType paramType, /// Static, Dynamic or Dynamic32, depending on the parameter type
    bytes[] calldata compValues /// The reference values used while comparing and authorizing
)
```

```json
{
    "id": 25,
    "targetAddress": "0xd8dd9164E765bEF903E429c9462E51F0Ea8514F9",
    "contractName": "Roles",
    "functionSignature": "scopeParameterAsOneOf(uint16,address,bytes4,uint256,uint8,bytes[])",
    "functionDescription": "scopeParameterAsOneOf(uint16 role, address targetAddress, bytes4 functionSig, uint256 paramIndex, uint8 paramType, bytes[] compValues)",
    "functionSelector": "0x93933772",
    "params": {
        "role": 1,
        "targetAddress": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "targetAddressName": "Aave_v3: Pool",
        "functionSig": {
            "selector": "0x617ba037",
            "signature": "supply(address,uint256,address,uint16)",
            "description": "supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)"
        },
        "paramIndex": 0,
        "paramType": "0: Static",
        "compValues": [
            "0x0000000000000000000000006b175474e89094c44da98b954eedeac495271d0f",
            "0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
        ]
    }
}
```


## Configuration


- Install the python dev dependencies: `pip install -r requirements.txt` - while located in the directory containing the library
- Follow the `Configuration` options for [defyes](https://github.com/karpatkey/defyes) installed as required package
    - First you will have to modify the [config.json](https://github.com/KarpatkeyDAO/defyes/blob/main/defyes/config.json)
    - You should provide `RPC` endpoints and `EXPLORER_API_KEYS`
    - You should set the env `CONFIG_PATH` env with the config.json's absolute path or the config.json can be placed under default package path `/path/to/python/site-packages/defyes/config.json`
- The file `dune_labels.json` is provided with labels generated by [this](https://dune.com/queries/3173156) Dune query
    - A request can be done to the Dune API to generate the JSON file ad-hoc (and thus override the provided one with a user-generated one) by providing a Dune API Key
    - First you will have to modify the [config.json](https://github.com/karpatkey/payload_decoder_v1/blob/main/payload_decoder_v1/utils/config.json) located in `payload_decoder_v1/utils` (not the one mentioned in defyes, since they are different files)
    - You should provide `DUNE_API_KEYS`
    - You should set the env `DECODER_CONFIG_PATH` env with the config.json's absolute path or the config.json can be placed under default repo path
    - If an API key is provided then the JSON file will be generated with the execution of the script. If not, the provided labels will be used


**NOTES:**
- Installing `requirements.txt` seems to fail with `python==3.12.0` but works fine with `python==3.11.5`
- Dune API request consumes approximately 800 credits
- `dune_labels.json` can't be and empty file (at most an emtpy JSON: `{}`)


## Usage


- Run the script with the command `python payload_decoder_v1/payload_decoder.py`
- Provide the `path` to the JSON file (you will be asked for it)
- File will be decoded and compiled into a JSON `payload_decoder_v1` subfolder
