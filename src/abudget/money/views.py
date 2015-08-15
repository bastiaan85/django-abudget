from braces.views import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView, View
from django.shortcuts import redirect

from .forms import TransactionForm, IncomeForm
from .models import Transaction, Income


class TransactionsView(LoginRequiredMixin, TemplateView):
    template_name = 'money/transactions.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TransactionsView, self).get_context_data(*args, **kwargs)

        stat_spent = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_income = Income.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        stat_balance = stat_income - stat_spent

        context['stat_spent'] = stat_spent
        context['stat_income'] = stat_income
        context['stat_balance'] = stat_balance

        transactions = Transaction.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        )

        context['new_transaction_form'] = TransactionForm()
        context['transactions'] = transactions
        return context


class TransactionsCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'money/transactions.html'

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(TransactionsCreateView, self).get_form_kwargs(*args, **kwargs)

        # TODO: right workflow here
        # TODO: error handling here
        form_kwargs['budget'] = self.request.budget
        form_kwargs['creator'] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse('money:transactions')


class TransactionsRemoveView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(
            id=request.POST.get('transaction_id'),
            budget=request.budget
        )
        transaction.delete()
        return HttpResponse('ok')


class IncomeView(LoginRequiredMixin, TemplateView):
    template_name = 'money/income.html'

    def get_context_data(self, *args, **kwargs):
        context = super(IncomeView, self).get_context_data(*args, **kwargs)

        context['new_income_form'] = IncomeForm()
        context['transactions'] = Income.objects.filter_by_date(self.request).filter(
            budget=self.request.budget,
        )
        return context


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    # TODO: exception if form invalid

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super(IncomeCreateView, self).get_form_kwargs(*args, **kwargs)
        # TODO: right workflow here
        # TODO: error handling here
        form_kwargs['budget'] = self.request.budget
        form_kwargs['creator'] = self.request.user
        return form_kwargs

    def get_success_url(self):
        return reverse('money:income')


class UpdateFilterView(View):

    def post(self, request, *args, **kwargs):
        redirect_url = request.POST.get('redirect_to')
        filter_by = request.session.get('filter_by', {'date': 'this_month'})
        filter_by['date'] = request.POST.get('date', 'this_month')
        request.session['filter_by'] = filter_by
        request.session.modified = True
        if not redirect_url[0] == '/':
            raise Exception()
        return redirect(redirect_url)
