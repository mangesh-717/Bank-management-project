from django import forms

class loginform(forms.Form):
    Email=forms.CharField()
    username= forms.CharField()
    password= forms.CharField(widget=forms.PasswordInput)
   


class LoanRequestForm(forms.Form):
    Username = forms.CharField(label='UserName', max_length=100)
    email = forms.EmailField(label='Email')
    amount = forms.DecimalField(label='Loan Amount')
    Loan_Tenure= forms.DecimalField(label='Loan Tenure')
    purpose_choices = [
        ('home', 'Home Purchase'),
        ('car', 'Car Loan'),
        ('education', 'Education'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    purpose = forms.ChoiceField(label='Loan Purpose', choices=purpose_choices)
    message = forms.CharField(label='Additional Information', widget=forms.Textarea)


from .models import HelpData
class HelpDesk(forms.ModelForm):
    class Meta:
        model=HelpData
        # fields = ['email', 'issue']

        fields='__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'required': 'true'}),
            'issue': forms.Textarea(attrs={'required': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super(HelpDesk, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['issue'].required = True