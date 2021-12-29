import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Coin(models.Model):
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.description
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class MineAmount(models.Model):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    MineAmount_text = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.MineAmount_text

class Account(models.Model):
    miner = models.ForeignKey(User, on_delete=models.CASCADE)
    ProcessingPower = models.IntegerField(default=100)

class CoinAmount(models.Model):
    miner = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

class MiningTransaction(models.Model):
    coin_text = models.CharField(max_length=200)
    amount_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.coin_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)