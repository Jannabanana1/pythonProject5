import hashlib

class Block:
    def __init__(self, index, timestamp, content, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.content = content
        self.previous_hash = previous_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.content).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()


M4BlockChain = []

from datetime import datetime


def create_genesis_block():
    return Block(0, datetime.now(), "Genesis Block", "0")


M4BlockChain.append(create_genesis_block())


# write a function `next_block` to generate a block
def next_block(last_block):
    #loop
    string = "this is block " + last_block.index+1
    return Block(last_block.index+1, datetime.now(), string, last_block.hash)



# append 5 blocks to the blockchain
def app_five(block_list):
    for i in range(5):
        block_list.append(next_block(block_list[-1]))

#just
#In the file linked_list.py, you need to define two functions “next_block” and “app_five.”
#The “next_block” function takes as input a block (a Python object of class Block) and
#returns a new block that follows the block provided.
# Your “next_block” function should set
#the index of the next block to be the index of the previous block plus one, the timestamp
#should be the current time, and the content should be string “this is block i” where i is the index of the block.
#The “app_five” function should take an existing chain “block_list” and append five blocks to it.
#The function app_five should modify block list directly, and does not need to return anything.