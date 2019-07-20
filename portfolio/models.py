from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import requests
from decimal import Decimal


# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return self.recent_value - self.acquired_value


class Stock(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField(max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return self.shares * self.purchase_price

    def current_stock_price(self):
        symbol_f = str(self.symbol)
        main_api = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
        api_key = '&apikey= JNO0VT6F5XU1HWZU'
        url = main_api + symbol_f + api_key
        json_data = requests.get(url).json()

        print('STOCK', api_key, json_data, '\n')

        open_price = json_data.get('Global Quote', {}).get("05. price", self.purchase_price)
        share_value = open_price
        return share_value

    def current_stock_value(self):
        return round((Decimal(self.current_stock_price()) * Decimal(self.shares)), 3)


class MutualFund(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='mutual_funds')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField(max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_mutual_fund_value(self):
        return self.shares * self.purchase_price

    def current_mutual_fund_price(self):
        mf_symbol_f = str(self.symbol)
        mf_main_api = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='
        mf_api_key = '&apikey=GOMG8YHN1JRNWXZO'
        mf_url = mf_main_api + mf_symbol_f + mf_api_key
        mf_json_data = requests.get(mf_url).json()
        print('MF', mf_api_key, mf_json_data, '\n')
        mf_open_price = mf_json_data.get('Global Quote', {}).get("05. price", self.purchase_price)
        mf_share_value = mf_open_price
        return mf_share_value

    def current_mutual_fund_value(self):
        return round((Decimal(self.current_mutual_fund_price()) * Decimal(self.shares)), 3)

