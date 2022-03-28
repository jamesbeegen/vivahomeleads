from django import forms
from .models import Lead, QualTable
from django.contrib.auth.models import User


class UpdateLog(forms.ModelForm):
    logtext = forms.CharField(widget=forms.Textarea()),

    class Meta:
        model = Lead
        fields = ['log']

        
class CreateLead(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=10, required=True, help_text="Don't include parentheses or dashes")
    email = forms.EmailInput()
    credit = forms.CharField(max_length=3, required=True)
    last_contacted = forms.DateField(widget=forms.DateInput, help_text="mm/dd/yyyy")
    last_contact_method = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'phone', 'email', 'credit', 'last_contacted', 'last_contact_method']

        
class EditLead(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=10, required=True, help_text="Don't include parentheses or dashes")
    email = forms.EmailInput()
    credit = forms.CharField(max_length=3, required=True)
    last_contacted = forms.DateField(widget=forms.DateInput, help_text="mm/dd/yyyy")
    last_contact_method = forms.CharField(max_length=30, required=True)
    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'phone', 'email', 'credit', 'last_contacted', 'last_contact_method']
        
        
class AdminEditLead(forms.ModelForm):
    user = forms.ChoiceField(choices = [(x, x) for x in User.objects.all()], required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=10, required=True, help_text="Don't include parentheses or dashes")
    email = forms.EmailInput()
    credit = forms.CharField(max_length=3, required=True)
    last_contacted = forms.DateField(widget=forms.DateInput, help_text="mm/dd/yyyy")
    last_contact_method = forms.CharField(max_length=30, required=True)

    class Meta:
        model = Lead
        fields = ['first_name', 'last_name', 'phone', 'email', 'credit', 'last_contacted', 'last_contact_method']
        
        
LOAN_TYPES = [
    'FHA',
    'Conventional',
]
DOWNPAYMENTS = [
    3.0, 3.5, 5.0, 10.0, 15.0, 20.0
]
TERMS = [360, 180]


class QualForm(forms.ModelForm):
    loan_type = forms.ChoiceField(choices = [(x, x) for x in LOAN_TYPES], required=True)
    price = forms.IntegerField(required=True, help_text="Enter the purchase price of the home (ex: 225000)")
    down_payment = forms.ChoiceField(choices = [(x,x) for x in DOWNPAYMENTS],
                                     help_text="Enter the percent of down payment (ex: 3.5 for FHA)",
                                     required=True)

    rate = forms.FloatField(required=True, help_text="Enter the interest rate (ex: 4.25)")
    HOA_dues = forms.FloatField(required=False, help_text='Enter monthly HOA dues if applicable')
    term = forms.ChoiceField(choices = [(x, x) for x in TERMS], required=True
                              ,help_text='Enter "360" for 30-year mortgage')
    monthly_payment = forms.FloatField(required=False,
                                       help_text = 'Includes estimated Homeowners insurance and monthly taxes')

    class Meta:
        model = QualTable
        fields = ['loan_type','price', 'down_payment', 'rate',
                  'HOA_dues', 'term', 'monthly_payment']

        
class DeleteLead(forms.ModelForm):
    class Meta:
        model = Lead
        fields = []

