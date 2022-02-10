from hashlib import sha256
import json
from time import time,sleep
import threading

class Block:
    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time()
        self.data = [] if data is None else data
        self.prevHash = None
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):
        hash = sha256()
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.getHash()
class Blockchain:
    def __init__(self):
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 30000
        self.counter = 0
        self.totaltime=0

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block,flag="not"):
        t1=time()
        self.flag=flag
        block.prevHash = self.getLastBlock().hash
        block.hash = block.getHash()
        block.mine(self.difficulty)

        self.chain.append(block)
        self.counter += 1

        self.difficulty += (-1, 1)[int(time()) - int(self.getLastBlock().timestamp) < self.blockTime]
        if flag == "attack" :
            sleep(2)
        else:
            sleep(1)

        t = time()-t1
        self.totaltime += t

    def isValid(self):
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
                return False
        return True
    def __repr__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp, 'nonce': item.nonce, 'hash': item.hash, 'prevHash': item.prevHash} for item in self.chain], indent=4)

bchain = Blockchain()
    # Add a new block
bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 100})))

attack_chain = Blockchain()
attack_chain.chain = bchain.chain
# attack_chain.totaltime = bchain.totaltime
bchain.totaltime=0

threading.Thread(target=attack_chain.addBlock(Block(str(int(time())), ({"from": "John", "to": "alice", "amount": 100})),"attack")).start()
threading.Thread(target=bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 75})))).start()
x=1
# threading.Thread(target=attack_chain.addBlock(Block(str(int(time())), ({"from": "John", "to": "alice", "amount": 25})),"attack")).start()
# threading.Thread(target=bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 150})))).start()


# print(bchain)
print("time required by attack to be successful {} sec".format(bchain.totaltime))
print("time taken by current attack to append new block is {} sec".format(attack_chain.totaltime))
bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 150})))
# bchain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 200})))
print("the real block chain")
print(bchain)
print("failed attack chain")
print(attack_chain)