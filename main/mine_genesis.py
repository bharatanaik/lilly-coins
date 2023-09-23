import hashlib
import json
from sys import getsizeof
from django.conf import settings
from main.models import Block, LillyUser, Transaction

def block_json(request, transaction_hashes):
    transactions = []
    for hash in transaction_hashes:
            transactions.append(Transaction.objects.get(hash = hash).get_transaction_data())
    json_data = json.dumps({
            "index":Block.objects.count()+1,
            "prev_hash":Block.objects.all().last().hash if Block.objects.count() != 0 else "",
            "miner":request.user.address,
            "difficulty":settings.MINING_DIFFICULTY,
            "transactions":transactions
        })
    return json_data


class ValidateBlock(object):

    def __init__(self,request,  transaction_hashes, hash, nonce) -> None:
        self.transaction_hashes = transaction_hashes
        self.hash = hash
        self.nonce = nonce
        self.request = request

    def get_json_data(self):
        json_data = block_json(self.request, self.transaction_hashes)
        return json_data

    def block_data(self):
        return json.loads(self.get_json_data())
 
    def validate(self) -> bool:
        data = self.block_data()
        data.update({
            "nonce":self.nonce
        })
        hash = hashlib.sha256(json.dumps(data).encode()).hexdigest()
        if hash == self.hash:
            return True
        else:
            return False




class BlockCreator(object):
    def __init__(self,request, hash, nonce, transaction_hashes) -> None:
        self.request = request
        self.hash = hash
        self.transaction_hashes = transaction_hashes
        self.nonce = nonce
        self.data = json.loads(block_json( request, transaction_hashes))
        try:
            self.main_user = LillyUser.objects.get(username = "main")
        except: 
            user = LillyUser(username = "main")
            user.set_password("*"*6)
            user.save()
            self.main_user = user
            
    def create_block(self):
        block = Block()
        block.index = self.data["index"]
        block.miner = self.request.user
        block.prev_hash = self.data["prev_hash"]
        block.hash = self.hash
        transactions = [Transaction.objects.get(hash=hash) for hash in self.transaction_hashes]
        self.confirm_transactions(transactions)
        block.no_of_transactions = len(transactions)
        block.nonce = self.nonce
        block.difficulty = self.data["difficulty"]
        block.block_reward = settings.MINING_REWARD
        block.block_size = getsizeof(self.data)
        block.save()
        block.transactions.add(*transactions)
        block.save()
        self.reward_miner()


    def confirm_transactions(self, transactions):
        for trans in transactions:
            trans.makeTransaction()
            trans.confirmed = True
            trans.save()

    def reward_miner(self):
        self.request.user.recieve_amount(settings.MINING_REWARD)
        Transaction.objects.create(
            sender = self.main_user,
            reciever = self.request.user,
            amount = settings.MINING_REWARD,
            confirmed = True
        )
