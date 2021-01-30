from django.urls import path

from .views import (
    TransactionHomeView,
    TransactionUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
   
    AdminUserView,
    ReportHome,
    ResultView,
    RepaymentHome,
    IncomeHome,
    ExpenseHome,
    Reports,
    ReportCreateView,
    ReportDeleteView,
    ReportUpdateView,
    myresultView,
    TransactionDetailView
    
 
)


urlpatterns = [


    path('', TransactionHomeView.as_view(), name='transaction_home'),

   

     path('users/', AdminUserView.as_view(), name='user'),
    
     path('transaction/new/', TransactionCreateView.as_view(),
         name='transaction_create'),
     
    path('transaction/<int:pk>/update/',
         TransactionUpdateView.as_view(), name='transaction_update'),
    
    path('transaction/<int:pk>/delete/',
         TransactionDeleteView.as_view(), name='transaction_delete'),

      path('transaction/<int:pk>/',
         TransactionDetailView.as_view(), name='transaction_detail'),    

    path('transactions/transactions/search/',
         ResultView.as_view(), name='transaction_search'),

     path('transactions/reports/search/',
         myresultView.as_view(), name='mysearch'),    
    
    path('reports/', ReportHome.as_view(), name='disbursements'),

    path('repayments/', RepaymentHome.as_view(), name='repayments'),

    path('income/', IncomeHome.as_view(), name='income'),

    path('Expense/', ExpenseHome.as_view(), name='expense'),



    path('monthlyreports/', Reports.as_view(), name='report'),
    
     path('report/new/', ReportCreateView.as_view(),
         name='report_create'),
     
    path('report/<int:pk>/update/',
         ReportUpdateView.as_view(), name='report_update'),
    
    path('report/<int:pk>/delete/',
         ReportDeleteView.as_view(), name='report_delete'),
]
