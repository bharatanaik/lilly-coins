import hashlib
import json, rsa
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from core.utils import sign

class LillyUser(AbstractUser):
    public_key = models.TextField(unique=True)
    private_key = models.TextField(unique=True)
    amount = models.IntegerField(default=0)
    address = models.CharField(max_length=32, unique=True)

    def get_private_key(self):
        return rsa.PrivateKey.load_pkcs1(self.private_key)

    def get_public_key(self):
        return rsa.PublicKey.load_pkcs1(self.public_key)

    def send_amount(self, amount):
        self.amount -= amount
        self.save()

    def recieve_amount(self,amount):
        self.amount += amount
        self.save()

    def save(self, *args, **kwargs) -> None:
        if len(self.address) != 32:
            PublicKey, PrivateKey = rsa.newkeys(1024)
            self.private_key = rsa.PublicKey.save_pkcs1(PrivateKey).decode("ascii")
            self.public_key = rsa.PublicKey.save_pkcs1(PublicKey).decode("ascii")
            self.address = hashlib.md5(self.private_key.encode()).hexdigest()
        return super().save(*args, **kwargs)

    
class Transaction(models.Model):
    sender = models.ForeignKey(LillyUser, on_delete=models.CASCADE, related_name="sender")
    reciever =  models.ForeignKey(LillyUser, on_delete=models.CASCADE, related_name="reciever")
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    signature = models.TextField()
    confirmed = models.BooleanField(default=False)
    hash = models.CharField(max_length=64)
    
    def signTransaction(self):
        private_key =self.sender.get_private_key()
        self.signature =  sign(self.calculateHash(), private_key)
        return self.signature

    def calculateHash(self):
        hashEncoded = json.dumps(self.get_data(), sort_keys=True).encode()
        return hashlib.sha256(hashEncoded).hexdigest()
    
    def makeTransaction(self):
        self.sender.send_amount(self.amount)
        self.reciever.recieve_amount(self.amount)

    def save(self,*args, **kwargs) -> None:
        self.signature = self.signTransaction()
        self.hash = self.get_hash()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.sender} - {self.reciever} - {self.amount}"

    def get_hash(self):
        return hashlib.sha256(json.dumps(self.get_transaction_data()).encode()).hexdigest()


    def get_data(self):
        return {
            "index":self.pk,
            "sender":self.sender.address,
            "reciever":self.reciever.address,
            "amount":self.amount,
            "timestamp":str(self.timestamp),
        }

    def get_confirmed(self):
        self.confirm = True
        self.save()

    def get_transaction_data(self):
        data = self.get_data()
        data.update({
            "index":self.pk,
            "signature":self.signature,
            "hash":self.hash
            })
        return data


class Block(models.Model):
    # serial number of block chain
    index = models.IntegerField()
    # User who mined
    miner = models.ForeignKey(LillyUser, on_delete=models.CASCADE)
    # Hash of previous block
    prev_hash = models.CharField(max_length = 64, verbose_name='Previous Hash')
    # Hash of the block
    hash = models.CharField(max_length = 64, verbose_name='Block Hash')
    # timestamp when block mined
    timestamp = models.DateTimeField(auto_now_add=True)
    # list of transactions
    transactions = models.ManyToManyField(Transaction)
    # number of transactions
    no_of_transactions = models.IntegerField()
    # number of times hash were generated
    nonce = models.CharField(max_length=1000)
    # number of zeroes in front of hash
    difficulty = models.IntegerField(default=settings.MINING_DIFFICULTY)
    # Block Reward
    block_reward = models.FloatField(default=settings.MINING_REWARD)
    # Block Size
    block_size = models.IntegerField()

        
