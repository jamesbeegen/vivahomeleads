from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from accounts.forms import ProfileForm, UserForm
from django.contrib import messages
from datetime import date
from .forms import CreateLead, EditLead, AdminEditLead,DeleteLead, QualForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import Lead, QualTable


admins = (
    'cgonzalez',
    'admin'
)


def home(request):
    return render(request, 'home.html')


def leads(request):
    user = request.user
    if user.username in admins:
        leads=Lead.objects.all()
    else:
        leads = Lead.objects.filter(user=user)
    return render(request, 'leads.html', {'leads': leads})


def logs(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    compare_log = lead.log
    if request.method == 'POST':
        log = request.POST["log"]
        if log != compare_log:
            lead.log = log + '\n-------- Entry created on {0}---------'.format(date.today())
            lead.save()
        return redirect('leads')
    else:
        return render(request, 'logs.html', {'lead': lead})

    
def qual_table(request, pk):

    lead = get_object_or_404(Lead, pk=pk)
    table = get_object_or_404(QualTable, lead_id=pk)
    form = QualForm(initial={
        'loan_type': table.loan_type,
        'price': table.price,
        'down_payment': table.down_payment,
        'rate': table.rate,
        'HOA_dues': table.HOA_dues,
        'term': table.term,
        'monthly_payment': get_payment(table)
    })
    if request.method == 'POST':
        form = QualForm(request.POST, instance=table)
        if form.is_valid():
            form.instance.lead = lead
            form.save()
            form = QualForm(initial={
                'loan_type': table.loan_type,
                'price': table.price,
                'down_payment': table.down_payment,
                'rate': table.rate,
                'HOA_dues': table.HOA_dues,
                'term': table.term,
                'monthly_payment': get_payment(table)
    })

            return render(request, 'loan_calc.html', {'form': form})
        else:
            form = QualForm(initial={
                'loan_type': table.loan_type,
                'price': table.price,
                'down_payment': table.down_payment,
                'rate': table.rate,
                'HOA_dues': table.HOA_dues,
                'term': table.term,
                'monthly_payment': get_payment(table)
            })
    return render(request, 'loan_calc.html', {'form': form})


def get_payment(table):
    MIP_UPFRONT = .0175
    hoi = (table.price * .0002)
    taxes = (table.price * .008) / 12
    if table.term <= 180:
        MIP_MONTHLY = .7 / 100
    else:
        MIP_MONTHLY = .8 / 100
    PMI_RATE = .000418  #AVERAGE

    #months of payments
    n = table.term

    #interest rate
    c = (table.rate / 100) / 12

    money_down = (table.down_payment / 100) * table.price
    loan_amount = (table.price - money_down)
    if table.loan_type == 'FHA':
        loan_amount += (loan_amount * MIP_UPFRONT)
        monthly = loan_amount *((c*(1+c)**n)/(((1+c)**n) - 1))
        monthly += (loan_amount * MIP_MONTHLY) / 12
    else:
        monthly = loan_amount * ((c*(1+c)**n)/(((1+c)**n) - 1))
        if table.down_payment < .2:
            monthly += (table.price * PMI_RATE)
    monthly += hoi + taxes + table.HOA_dues
    monthly = '{0:.2f}'.format(monthly)
    return monthly


def edit(request, pk):
    user = request.user
    lead = get_object_or_404(Lead, pk=pk)
    if user.username == 'admin' or user.username == 'Carlos':
        form = AdminEditLead(request.POST, instance=lead)
    else:
        form = EditLead(request.POST, instance=lead)
    if request.method == 'POST':
        if form.is_valid():
            if user.username == 'admin' or user.username == 'cgonzalez':
                new_user = request.POST['user']
                new_user = User.objects.get(username = new_user)
                lead.user = new_user
            form.save()
            return redirect('leads')
    else:
        if user.username == 'admin' or user.username== 'Carlos':
            form = AdminEditLead(initial={
                'user': lead.user,
                'first_name': lead.first_name,
                'last_name': lead.last_name,
                'phone': lead.phone,
                'email': lead.email,
                'credit': lead.credit,
                'last_contacted': lead.last_contacted.strftime("%m/%d/%Y"),
                'last_contact_method': lead.last_contact_method,
            })
        else:
            form = EditLead(initial={
                'first_name': lead.first_name,
                'last_name': lead.last_name,
                'phone': lead.phone,
                'email': lead.email,
                'credit': lead.credit,
                'last_contacted': lead.last_contacted.strftime("%m/%d/%Y"),
                'last_contact_method': lead.last_contact_method,
            })

    return render(request, 'edit.html', {'form': form})


def add_lead(request):
    user = request.user
    if request.method == 'POST':
        form = CreateLead(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.user = user
            lead.save()
            return redirect('leads')
    else:
        form = CreateLead()
    return render(request, 'add_lead.html', {'form': form})


def delete_lead(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == 'POST':
        form = DeleteLead(request.POST)
        if form.is_valid():
            lead.delete()
        return redirect('leads')
    else:
        form = DeleteLead()
        return render(request, 'delete.html', {'form': form})

    
@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('leads')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct errors below')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html',
                      {'form': form})
