from django.conf.urls import url

from .views import (
    TransactionsView, TransactionsCreateView, TransactionsRemoveView,
    IncomeView, IncomeCreateView, IncomeRemoveView,
    UpdateFilterView,
)

urlpatterns = [
    url(r'^$', TransactionsView.as_view(), name='transactions'),
    url(r'^income/$', IncomeView.as_view(), name='income'),
    url(r'^income/create/$', IncomeCreateView.as_view(), name='income_create'),
    url(r'^income/remove/$', IncomeRemoveView.as_view(), name='income_remove'),
    url(r'^transactions/create/$', TransactionsCreateView.as_view(), name='transaction_create'),
    url(r'^transactions/remove/$', TransactionsRemoveView.as_view(), name='transaction_remove'),

    url(r'^update_filter/$', UpdateFilterView.as_view(), name='update_filter'),
]
