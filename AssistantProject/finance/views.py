from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
import json

@login_required(login_url='/login/')
def finance_home(request):
    # 1. Fetch user's data
    accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(account__user=request.user).order_by('-date')
    
    # ... (Keep the rest of your finance_home logic exactly the same) ...
    # 2. Initialize Forms
    a_form = AccountForm()
    t_form = TransactionForm()
    
    # Security/UX: Only let the user add transactions to THEIR accounts
    t_form.fields['account'].queryset = accounts

    # 3. Handle Button Clicks (POST requests)
    if request.method == 'POST':
        # Add Account
        if 'add_account' in request.POST:
            a_form = AccountForm(request.POST)
            if a_form.is_valid():
                account = a_form.save(commit=False)
                account.user = request.user  # Link wallet to logged-in user
                account.save()
                return redirect('finance_home')
        
        # Add Transaction
        elif 'add_transaction' in request.POST:
            t_form = TransactionForm(request.POST)
            if t_form.is_valid():
                tx = t_form.save()
                # Automatically update wallet balance
                if tx.is_income:
                    tx.account.balance += tx.amount
                else:
                    tx.account.balance -= tx.amount
                tx.account.save()
                return redirect('finance_home')
                
        # Edit Balance
        elif 'update_balance' in request.POST:
            acc_id = request.POST.get('account_id')
            new_balance = request.POST.get('new_balance')
            acc = get_object_or_404(Account, id=acc_id, user=request.user)
            acc.balance = new_balance
            acc.save()
            return redirect('finance_home')

        # Delete Transaction
        elif 'delete_tx' in request.POST:
            tx_id = request.POST.get('tx_id')
            tx = get_object_or_404(Transaction, id=tx_id, account__user=request.user)
            # Revert the money before deleting
            if tx.is_income:
                tx.account.balance -= tx.amount
            else:
                tx.account.balance += tx.amount
            tx.account.save()
            tx.delete()
            return redirect('finance_home')
            
        # Delete Account
        elif 'delete_acc' in request.POST:
            acc_id = request.POST.get('acc_id')
            acc = get_object_or_404(Account, id=acc_id, user=request.user)
            acc.delete()
            return redirect('finance_home')

    # 4. Calculate Net Worth & Totals (The missing numbers!)
    total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
    income_total = transactions.filter(is_income=True).aggregate(Sum('amount'))['amount__sum'] or 0
    expense_total = transactions.filter(is_income=False).aggregate(Sum('amount'))['amount__sum'] or 0

    # 5. Calculate Chart Data
    expenses = transactions.filter(is_income=False)
    labels = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Other']
    data = []
    for label in labels:
        total = expenses.filter(category=label).aggregate(Sum('amount'))['amount__sum'] or 0
        data.append(float(total))

    # 6. Send everything to the HTML
    context = {
        'accounts': accounts,
        'transactions': transactions,
        'a_form': a_form,
        't_form': t_form,
        'total_balance': total_balance,
        'income_total': income_total,
        'expense_total': expense_total,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    return render(request, 'finance/home.html', context)