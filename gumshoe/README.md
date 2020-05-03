# gumshoe

Investigates bytecode for fishy behaviour.

## ideas of things to flag
- using uniswap v1 as a price oracle
- value secured > value securing oracles (or smth)
- detect admin/owner
  - esp. owner self-destruct, owner migrate..patterns
- detect non-compliant ERC20s/721s/etc.
- detect timelock for governance (?)