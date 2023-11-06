# Payload Decoder v1

​
Payload Decoder v1 is a Python library designed to decode payloads for [Roles Modifier v1](https://github.com/gnosis/zodiac-modifier-roles-v1), developed by [Gnosis Guild](https://www.gnosisguild.org/).
​

## Zodiac Roles Modifier

​
The Roles Modifier belongs to the [Zodiac](https://github.com/gnosis/zodiac) collection of tools, which can be accessed through the Zodiac App available on [Gnosis Safe](https://gnosis-safe.io/), as well as in the Zodiac repository.
​
If you have any questions about Zodiac, join the [Gnosis Guild Discord](https://discord.gg/wwmBWTgyEq). Follow [@GnosisGuild](https://twitter.com/gnosisguild) on Twitter for updates.
​

### About the Roles Modifier

​
This modifier allows avatars to enforce granular, role-based, permissions for attached modules.
​
Modules that have been granted a role are able to unilaterally make calls to any approved addresses, approved functions, and approved variables the role has access to.
​
The interface mirrors the relevant parts of the Gnosis Safe's interface, so this contract can be placed between Gnosis Safe modules and a Gnosis Safe to enforce role-based permissions.
​

### Entities

​
Thanks to [p2p.org](https://p2p.org/) for the entities concept.
​

- **Zodiac Roles Modifier (Roles)** is contract developed by Gnosis Guild for non-custodial asset management. `Zodiac` is the name of the toolset. `Roles` is the name of the top-level contract. `Modifier` is a base contract for a subset of Zodiac tools, including Roles.
- **Avatar** (in Zodiac jargon) is an address that can be “piloted” meaning a certain action (contract call) can be made on its behalf by Pilot via Roles.
- **Pilot** (in Zodiac jargon) is an address approved by Avatar to do a certain action on its behalf via Roles.
  ​

## Roles.sol

​
Contains the functions that are exposed to being called by an Ethereum account. For creating/modifying/eliminating permissions granted to the Pilot account, `scoping` functions are called in the Roles contract deployed by the Avatar Safe (and can only be called by the owner).<br>
​
This functions, their parameters and their execution consequences can be found in the [Roles Modifier v1](https://github.com/gnosis/zodiac-modifier-roles-v1) repo and in each of the contract deployments made by Avatar's implementing the standard.
​
The main `scoping` functions called in any payload are described next.
​

### `scopeTarget`

​
To interact with contracts they have to be scoped first (the contract address).
​
`scopeTarget` scopes calls to an address, limited to specific function signatures, and per function scoping rules.
​

```solidity
function scopeTarget(
    uint16 role, /// Role to set for
    address targetAddress /// Address to be scoped
)
```

​

### `revokeTarget`

​
If no interactions are further needed with certain contracts they can be revoked, meaning the role no longer has permission interact with it.
​
`revokeTarget` disallows all calls made to an address
​

```solidity
function revokeTarget(
    uint16 role, /// Role to set for
    address targetAddress /// Address to be disallowed
)
```

​

### `scopeAllowFunction`

​
In order to call functions in scoped targets (contracts), functions have to be scoped.
​
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

​

### `scopeRevokeFunction`

​
Similar to `revokeTarget`, if specific function calls are no longer needed they can be revoked, meaning the role no longer has permission to interact with it.
​
`scopeRevokeFunction` disallows a specific function signature on a scoped target (disables the whitelisting of a scoped function).
​

```solidity
function scopeRevokeFunction(
    uint16 role, /// Role to set for
    address targetAddress, /// Scoped address on which a function signature should be disallowed
    bytes4 functionSig /// Function signature to be disallowed
)
```

​

### `scopeFunction`

​
Works the same way as `scopeAllowFunction`, but allows for constraining of call paramters only to single values.
​
`scopeFunction` sets scoping rules for a function, on a scoped address.
​

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

​

### `scopeParameterAsOneOf`

​
`scopeParameterAsOneOf` sets and enforces scoping rules, for a single parameter of a function, on a scoped target. (constraining the argument to be an element belonging in a given set). Parameter will be scoped with comparison type OneOf.
​

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

​

## Payload Decoder v1 Configuration

- Install the python dev dependencies: `pip install -r requirements.txt` - while located in the directory containing the library
- Follow the `Configuration` options for [defyes](https://github.com/karpatkey/defyes) installed as required package - First you will have to modify the [config.json](https://github.com/KarpatkeyDAO/defyes/blob/main/defyes/config.json) - You should provide `RPC` endpoints and `EXPLORER API KEYS` - You should set the env `CONFIG_PATH` env with the config.json's absolute path or the config.json can be placed under default package path `/path/to/python/site-packages/defyes/config.json`
  ​

## Usage

- Run the script with the command `python payload_decoder_v1/payload_decoder.py`
- Provide the `path` to the JSON file (you will be asked for it)
- File will be decoded and compiled into a JSON `payload_decoder_v1` subfolder
- An example output can be seen at `sample_audit.json`. Permissions follow no particular model, but `scopeFunction` and `scopeParameterAsOneOf` calls are complimentary to get an idea of how they are combined.
