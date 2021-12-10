import hashlib
import time


class Block:

    def __init__(self, index, proof_no, prev_hash, data, timestamp=None):
        self.index = index
        self.proof_no = proof_no
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculate_hash(self):
        block_of_string = str(self.index) + str(self.proof_no) + str(self.prev_hash) + str(self.data) + str(
            self.timestamp)
        return hashlib.sha256(block_of_string.encode()).hexdigest()

    def __repr__(self):
        return f"{self.index} - {self.proof_no} - {self.prev_hash} - {self.data} - {self.timestamp}"


class BlockChain:

    def __init__(self):
        self.chain = []
        self.current_data = []
        self.nodes = set()
        self.construct_genesis()

    def construct_genesis(self):
        self.construct_block(0, 0)

    def construct_block(self, proof_no, prev_hash):
        """
        Adds a block to the Blockchain
        :param proof_no:
        :param prev_hash:
        :return:
        """
        block = Block(index=self.chain, proof_no=proof_no, prev_hash=prev_hash, data=self.current_data)
        self.current_data = []
        self.chain.append(block)
        return block

    @staticmethod
    def check_validity(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False

        if prev_block.calcuate_hash != block.prev_hash:
            return False

        if not BlockChain.verifying_proof(block.proof_no, prev_block.proof_no):
            return False

        if block.timestamp <= prev_block.timestamp:
            return False

        return True

    def new_data(self, sender, recipient, quantity):
        self.current_data.append({"sender": sender, "recipient": recipient, "quantity": quantity})
        return True

    @staticmethod
    def proof_of_work(last_proof):
        proof_no = 0
        while BlockChain.verifying_proof(proof_no, last_proof) is False:
            proof_no += 1

        return proof_no

    @staticmethod
    def verifying_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    @staticmethod
    def construct_proof_of_work(prev_proof):
        pass

    @property
    def latest_block(self):
        return self.chain[-1]

    def block_mining(self, details_miner):
        self.new_data(sender=0, recipient=details_miner, quantity=1)

        last_block = self.latest_block
        last_proof_no = last_block.proof_no
        proof_no = self.proof_of_work(last_proof_no)

        last_hash = last_block.calculate_hash
        block = self.construct_block(proof_no, last_hash)

        return vars(block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @staticmethod
    def obtain_block_object(block_data):
        return Block(block_data['index'],
                     block_data['proof_no'],
                     block_data['prev_hash'],
                     block_data['data'],
                     timestamp=block_data['timestamp'])
