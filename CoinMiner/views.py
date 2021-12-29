from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import MineAmount, Coin, Account, CoinAmount, MiningTransaction
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone

#=============================================================================================[ERROR]
@login_required
def error(request):
    return render(request, 'CoinMiner/error.html')


#============================================================================================

#============================================================================================[ADD]
# FLAW 1: INJECTION (OWASP 2017-A01)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@csrf_exempt
@login_required
def add(request):
    miner = Account.objects.filter(miner=request.user)
    miner0 = miner[0]
    print(miner)
    
    if (request.method == 'POST'):
        print(miner0.id)
        add = request.POST['add']
        print(add)


        query = '''
        UPDATE CoinMiner_account 
        SET ProcessingPower = %s 
        WHERE miner_id = %s;
        ''' % (add, miner0.miner_id)
        with connection.cursor() as cursor:
            cursor.executescript(query)
            connection.commit()
            connection.close()

        return redirect("/CoinMiner")


    miner0.ProcessingPower += 1
    miner0.save()

    return render(request, 'CoinMiner/add.html')
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#============================================================================================

#============================================================================================[INDEX]
# FLAW 3: SENSITIVE DATA EXPOSURE (OWASP 2017-A03)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required
def index(request):
    latest_coin_list = Coin.objects.order_by('-pub_date')#[:5]
    miner = Account.objects.filter(miner=request.user)
    print(request.user)
    print(miner[0].miner)
    pp = miner[0].ProcessingPower
    print(pp)
    coinAmount = CoinAmount.objects.filter(miner=request.user)
    print(coinAmount[0].miner)
    print(coinAmount[0].coin)
    print(coinAmount[0].amount)
    amount = coinAmount[0].amount

    accounts = Account.objects.values()

    context = {'latest_coin_list': latest_coin_list, 'accounts':accounts, 'user':request.user, 'pp':pp, 'coinAmount':coinAmount}
    return render(request, 'CoinMiner/index.html', context)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#============================================================================================

#============================================================================================[DETAIL]
@login_required
def detail(request, coin_id):
    coin = get_object_or_404(Coin, pk=coin_id)
    miner = Account.objects.filter(miner=request.user)
    pp = miner[0].ProcessingPower
    return render(request, 'CoinMiner/detail.html', {'coin': coin, 'pp':pp})
#============================================================================================

#============================================================================================[RESULTS]
# FLAW 2: BROKEN ACCESS CONTROLS (OWASP 2017-A05)
# FLAW 5: CROSS-SITE SCRIPTING XSS (OWASP 2017-07)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def results(request, coin_id, message):
    coin = get_object_or_404(Coin, pk=coin_id)
    if (request.GET.get('message')):
        message = request.GET.get('message')
    print(message)
    mt = MiningTransaction(coin_text = coin.description, amount_text = message, pub_date=timezone.now())
    mt.save()
    print(mt.amount_text)

    latest_mt_list = MiningTransaction.objects.order_by('-pub_date')[:5]

    return render(request, 'CoinMiner/results.html', {'coin': coin, 'message': message, 'latest_mt_list':latest_mt_list})
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#============================================================================================

#============================================================================================[MINE]
# FLAW 5: CROSS-SITE SCRIPTING XSS (OWASP 2017-07)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@csrf_exempt
def mine(request, coin_id):
    
    # Getting the Account, CoinAmount, Coin - objects
    # Account will tell who the transaction is to be made for
    # Coin tells us which object we need to mine
    # CoinAmount is the object that tells us how much an account has of a given coin
    #-------------------------------------------------------------------
    # Account
    if(request.method == 'GET'):
        account = Account.objects.filter(miner=request.GET.get('user'))
    else:
        account = Account.objects.filter(miner=request.user)
    account0 = account[0]
    print(account0.miner.username)
    # Coin
    coin = get_object_or_404(Coin, pk=coin_id)
    # CoinAmount
    if(request.method == 'GET'):
        coinAmount = CoinAmount.objects.filter(miner=request.GET.get('user'), coin=coin_id)
    else:
        coinAmount = CoinAmount.objects.filter(miner=request.user, coin=coin_id)
    coinAmount0 = coinAmount[0]
    #-------------------------------------------------------------------


    #Getting the amount to be mined in this transaction
    #-------------------------------------------------------------------
    if(request.method == 'GET'):
        selected_mineAmount = 50
        print(selected_mineAmount)
    else:
        selected_mineAmount = request.POST['mineamount']
    #-------------------------------------------------------------------    


    # If we find an error in the amount to be mined, return the error page
    #-------------------------------------------------------------------
    message = str(selected_mineAmount)
    if not(selected_mineAmount):
        return render(request, 'CoinMiner/error.html', {'message': message})
    testStr = str(selected_mineAmount)    
    if not(testStr.isnumeric()):
        return render(request, 'CoinMiner/error.html', {'message': message})
    #--------------------------------------------------------------------


    # Checking that the miner has sufficient processing power to go through with the transaction
    #---------------------------------------------------------------------
    pp = account0.ProcessingPower
    s = int(selected_mineAmount)
    #print("pp - s: ")
    #print(pp - s)

    if (pp - s < 0):
        return render(request, 'CoinMiner/error.html', {'message': int(message)})
    #---------------------------------------------------------------------

    # Adding the amount mined to the amount of the coin, which the account holds
    #---------------------------------------------------------------------
    a = coinAmount0.amount        
    ap = a + s

    query = 'UPDATE CoinMiner_coinamount SET amount = %s WHERE miner_id = %s AND coin_id = %s' % (ap, coinAmount0.miner.id, coinAmount0.coin.id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        connection.commit()

    query = 'SELECT * FROM CoinMiner_coinamount WHERE miner_id = %d AND coin_id = %d' % (coinAmount0.miner.id, coinAmount0.coin.id)
    with connection.cursor() as cursor:
        s = cursor.execute(query)
        for row in s:
            print(row)
        connection.close()

    account0.ProcessingPower -= int(selected_mineAmount)
    account0.save()
    #---------------------------------------------------------------------


    return HttpResponseRedirect(reverse('CoinMiner:results', args=(coin.id, message)))
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#============================================================================================


