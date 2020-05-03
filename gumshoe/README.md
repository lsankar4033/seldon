# gumshoe

Investigates bytecode for fishy behaviour.

## ideas of things to flag
- using uniswap v1 as a price oracle
  - value secured > value securing oracles (or smth)
- detect admin/owner
  - esp. owner self-destruct, owner migrate..patterns

## plan
1. use rattle to produce block graph
2. define flags by existence of subgraphs in the block graph

For example, an admin owner is defined by:
1. storing caller in the constructor at A
2. JUMPIF on what's at A for the execution of any function
