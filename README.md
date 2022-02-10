# block-chain
Implement a blockchain Python application that keeps track of blockchain branches and appends new  blocks to the longest branch. In order to append a block, the block contain a 64bit nonce that causes the  hash to start with N zeros. Each block should contain a random list of transactions. Objectives: 1) Control the puzzle hardness by varying N so that the block chain grows at 1 block per second. 2) Simulate an attack on the blockchain: There is a chance that an attacker appears and tries to grow  his own branch of the blockchain, by appending to a previous block (not the latest verified block). The attack speed is a predetermined parameter. 3) By experimentation, find the attack speed where an attack is successful (the main branch is  replaced with the attacker’s branch), and compare it to the legit blockchain speed.