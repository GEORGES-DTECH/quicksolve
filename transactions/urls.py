from django.urls import path

from .views import (
    TransactionHomeView,
    TransactionUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
    AdminHomeView,
    AdminUserView,
    ReportHome,
    ResultView,
    RepaymentHome,
    IncomeHome
    
 
)


urlpatterns = [


    path('', TransactionHomeView.as_view(), name='transaction_home'),

    path('root/', AdminHomeView.as_view(), name='admin'),

     path('users/', AdminUserView.as_view(), name='user'),
    
     path('transaction/new/', TransactionCreateView.as_view(),
         name='transaction_create'),
     
    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction_update'),
    
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction_delete'),

    path('transactions/transaction/search/',
         ResultView.as_view(), name='transaction_search'),
    
    path('reports/', ReportHome.as_view(), name='disbursements'),

    path('repayments/', RepaymentHome.as_view(), name='repayments'),

    path('income/', IncomeHome.as_view(), name='income'),
]
