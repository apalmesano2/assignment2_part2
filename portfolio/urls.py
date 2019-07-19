from django.conf.urls import url
from . import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    # urls for Customers
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('customer/create/', views.customer_new, name='customer_new'),
    url(r'^customers_json/', views.CustomerList.as_view()),
    # urls for Investments
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('investment/create/', views.investment_new, name='investment_new'),
    # urls for Stocks
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('stock/create/', views.stock_new, name='stock_new'),
    # urls for Mutual Funds
    path('mutual_fund_list', views.mutual_fund_list, name='mutual_fund_list'),
    path('mutual_fund/<int:pk>/edit/', views.mutual_fund_edit, name='mutual_fund_edit'),
    path('mutual_fund/<int:pk>/delete/', views.mutual_fund_delete, name='mutual_fund_delete'),
    path('mutual_fund/create/', views.mutual_fund_new, name='mutual_fund_new'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
