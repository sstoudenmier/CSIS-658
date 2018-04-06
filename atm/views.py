from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.views.generic.base import View

from .models import Account

class IndexView(View):
    template_name = 'atm/index.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : 'Disabled',
        'right_button3_state' : 'Disabled',
        'right_button4_state' : 'Disabled',

        'number_button_state' : 'Disabled',

        'enter_button_state' : '',
        'clear_button_state' : 'Disabled',
        'cancel_button_state' : 'Disabled',
    }

    def is_valid_account(self, account_id):
        accounts = Account.objects.filter(account_id=account_id)
        if len(accounts) == 1:
            return True
        return False

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        account_id = request.POST['account_id']
        request.session['account_id'] = account_id
        if self.is_valid_account(account_id):
            return HttpResponse('valid')
        return HttpResponse('invalid')


class PinView(View):
    template_name = 'atm/pin.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : 'Disabled',
        'right_button3_state' : 'Disabled',
        'right_button4_state' : 'Disabled',

        'number_button_state' : '',

        'enter_button_state' : '',
        'clear_button_state' : '',
        'cancel_button_state' : '',
    }

    def is_valid_pin(self, account_id, pin):
        accounts = Account.objects.filter(account_id=account_id, account_pin=pin)
        if len(accounts) == 1:
            return True
        return False

    def post(self, request):
        account_id = request.session['account_id']
        account_pin = request.POST['account_pin']
        if self.is_valid_pin(account_id, account_pin):
            return HttpResponse('valid')
        return HttpResponse('invalid')

    def get(self, request):
        return render(request, self.template_name, self.context)


class TransactionView(View):
    template_name = 'atm/transaction.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : '',
        'right_button3_state' : '',
        'right_button4_state' : '',

        'number_button_state' : 'Disabled',

        'enter_button_state' : 'Disabled',
        'clear_button_state' : 'Disabled',
        'cancel_button_state' : '',
    }

    def get(self, request):
        return render(request, self.template_name, self.context)

class BalanceView(View):
    template_name = 'atm/balance.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : 'Disabled',
        'right_button3_state' : 'Disabled',
        'right_button4_state' : 'Disabled',

        'number_button_state' : 'Disabled',

        'enter_button_state' : 'Disabled',
        'clear_button_state' : 'Disabled',
        'cancel_button_state' : ''
    }

    def get(self, request):
        balance = Account.objects.filter(account_id=request.session['account_id'])[0].balance
        self.context['balance'] = balance
        return render(request, self.template_name, self.context)


class WithdrawalView(View):
    template_name = 'atm/withdrawal.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : 'Disabled',
        'right_button3_state' : 'Disabled',
        'right_button4_state' : 'Disabled',

        'number_button_state' : '',

        'enter_button_state' : '',
        'clear_button_state' : '',
        'cancel_button_state' : ''
    }

    def post(self, request):
        if request.POST['withdraw_amount'] == '':
            return HttpResponse('invalid none')
        amount = int(request.POST['withdraw_amount'])
        if amount > self.context['balance']:
            return HttpResponse('invalid balance')
        if amount > self.context['daily_limit']:
            return HttpResponse('exceeded limit')
        if amount % 10 != 0:
            return HttpResponse('invalid amount')
        account = Account.objects.filter(account_id=request.session['account_id'])[0]
        account.balance = self.context['balance'] - amount
        account.save()
        return HttpResponse(account.balance)

    def get(self, request):
        balance = Account.objects.filter(account_id=request.session['account_id'])[0].balance
        daily_limit = Account.objects.filter(account_id=request.session['account_id'])[0].daily_limit
        self.context['balance'] = float(balance)
        self.context['daily_limit'] = float(daily_limit)
        return render(request, self.template_name, self.context)


class DepositView(View):
    template_name = 'atm/deposit.html'
    context = {
        'left_button1_state' : 'Disabled',
        'left_button2_state' : 'Disabled',
        'left_button3_state' : 'Disabled',
        'left_button4_state' : 'Disabled',

        'right_button1_state' : 'Disabled',
        'right_button2_state' : 'Disabled',
        'right_button3_state' : 'Disabled',
        'right_button4_state' : 'Disabled',

        'number_button_state' : '',

        'enter_button_state' : '',
        'clear_button_state' : '',
        'cancel_button_state' : '',

        'enter_funds' : False
    }

    def post(self, request):
        if request.POST['inserted_amount'] != '' and not self.context['enter_funds']:
            return HttpResponse('jammed')
        if request.POST['deposit_amount'] == '':
            return HttpResponse('no deposit amount')
        if request.POST['inserted_amount'] == '' and self.context['enter_funds']:
            return HttpResponse('no inserted amount')
        if not self.context['enter_funds']:
            self.context['enter_funds'] = True
            return HttpResponse('insert deposit')
        inserted = int(request.POST['inserted_amount'])
        amount = int(request.POST['deposit_amount'])
        if amount != inserted:
            return HttpResponse('deposit and inserted mismatch')
        account = Account.objects.filter(account_id=request.session['account_id'])[0]
        account.balance = self.context['balance'] + amount
        account.save()
        self.context['enter_funds'] = False
        return HttpResponse(account.balance)

    def get(self, request):
        balance = Account.objects.filter(account_id=request.session['account_id'])[0].balance
        self.context['balance'] = float(balance)
        return render(request, self.template_name, self.context)