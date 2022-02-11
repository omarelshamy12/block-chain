from hashlib import sha256
import json
from time import time, sleep
import threading


class Block:

    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time()
        self.data = [] if data is None else data
        self.prevHash = None
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        blockHash = sha256()  # initially hash is empty

        # Hash converted into sequence of bytes using (.encode('utf-8')method)
        blockHash.update(str(self.prevHash).encode('utf-8'))
        blockHash.update(str(self.timestamp).encode('utf-8'))
        blockHash.update(str(self.data).encode('utf-8'))
        blockHash.update(str(self.nonce).encode('utf-8'))
        return blockHash.hexdigest()  # Hash of a Block

    # Mine Function represent miners in the real cryptography Blockchain world
    def mine(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()


# Class Blockchain
class Blockchain:

    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 30000
        self.counter = 0
        self.totaltime = 0
        self.flag = "not"

    # Get the freshest Block (Latest block)
    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    # To add a block to block chain
    def addBlock(self, block, flag="not"):
        t1 = time()
        self.flag = flag

        # Unique sequence number of a new Block is the PrevHash of the last block
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()  # Block Hash (messages and transactions itself)
        block.mine(self.difficulty)  # Check PoW from difficulty in mine function before adding Block to chain

        # add the block to chain
        self.chain.append(block)
        self.counter += 1

        # using python ternary operator (if_test_is_false, if_test_is_true)[test]
        self.difficulty += (-1, 1)[int(time()) - int(self.getLastBlock().timestamp) < self.blockTime]
        if flag == "attack":
            sleep(2)
        else:  # To generate block every 1 sec
            sleep(1)

        t = time() - t1
        self.totaltime += t

    # Check validity of block
    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]  # get currentBlock
            prevBlock = self.chain[i - 1]  # get previousBlock

            # CHECK if Hash of a block not the same
            # OR sequece number of current block(prevHash) not equal previousBlock Hash
            # OR time stamp of current Block smaller than or equal previousBlock
            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash or
                    currentBlock.timestamp <= prevBlock.timestamp):
                return False

        return True

    @staticmethod
    def proof_of_work(last_proof):
        """
        this simple algorithm identifies a number f' such that hash(ff') contain 10 leading zeroes
         f is the previous f'
         f' is the new proof
         #Number of leading zeros is depending on the 64-bit nonce value
         (This condition must be achieved before adding block to chain)
         To increase difficulty and attacker can't get the right value and add his block to chain easily
         10 leading zeros is just an example (common:60 zeros)
        """

        proof_no = 0
        while Blockchain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    # Verifying proof of work
    @staticmethod
    def verifying_proof(last_proof, proof):
        # verifying the proof: does Hash(last_proof, proof) contain 10 leading zeroes?

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:10] == "0000000000"

    def __repr__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp, 'nonce': item.nonce, 'hash': item.hash,
                            'prevHash': item.prevHash} for item in self.chain], indent=4)


# Main --To test The code
# the Real Block Chain
bchain = Blockchain()

# Add a new block to trusted chain
bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 100})))

# Attacker make Untrusted chain
attack_chain = Blockchain()
attack_chain.chain = bchain.chain
# attack_chain.totaltime = bchain.totaltime
bchain.totaltime = 0

threading.Thread(target=attack_chain.addBlock(Block(str(int(time())), ({"from": "John", "to": "alice", "amount": 100})),
                                              "attack")).start()
threading.Thread(target=bchain.addBlock(Block(str(int(time())),
                                              ({"from": "John", "to": "Bob", "amount": 75})))).start()
x = 1


# print(bchain)
print("time required by attack to be successful {} sec".format(bchain.totaltime))
print("time taken by current attack to append new block is {} sec".format(attack_chain.totaltime))
bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 150})))
# bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 200})))
print("the real block chain")
print(bchain)
print("failed attack chain")
print(attack_chain)
