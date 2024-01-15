from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Bankusers(models.Model):
    ACCOUNT_CHOICES = [
        ('Savings', 'Savings Account'),
        ('Checking', 'Current Account'),
        ('Student', 'Student Account'),
        ('Business', 'Business Account'),
        ('Loan', 'Loan Account'),
    ]
    account_type = models.CharField(max_length=40, choices=ACCOUNT_CHOICES)
    Users=models.ForeignKey(User,on_delete=models.SET_NULL , null=True , blank=True)# CASCADE SET_NULL SET_DEFAULT)
    phon=models.BigIntegerField()
    photo=models.FileField(upload_to='image/')
    adhar=models.FileField(upload_to='adhar/')
    loan_amount=models.FloatField(null=True , blank=True)
    emi=models.FloatField( null=True , blank=True)

    current_balance = models.FloatField(default=0.00)
    account_number = models.BigIntegerField( unique=True)
   

    def save(self, *args, **kwargs):
        import uuid

        if not self.account_number:
            # Generate a 12-digit unique account number using uuid
            self.account_number = str(uuid.uuid4().int)[:12]

            # Ensure the account number is unique
            while Bankusers.objects.filter(account_number=self.account_number).exists():
                self.account_number = str(uuid.uuid4().int)[:12]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}--{self.account_number}"





class CardApplication(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE )
    creaditcard = models.BooleanField(default=False, null=True, blank=True)
    debitcard = models.BooleanField(default=False, null=True, blank=True)
    # Add other fields as needed

class LoanRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    Loan_Tenure=models.IntegerField(default=1)
    purpose_choices = [
        ('home', 'Home Purchase'),
        ('Helth', 'Helth Loan'),
        ('car', 'Car Loan'),
        ('education', 'Education'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]
    purpose = models.CharField(max_length=20, choices=purpose_choices)
    message = models.TextField()

#     def __str__(self):
#         return f"{self.user.username}'s Loan Request"

   

class HelpData(models.Model):
    email=models.EmailField(null=True, blank=True)
    issue = models.TextField()
    
    # Add other fields as needed




class Transaction(models.Model):
    bank_user = models.ForeignKey(Bankusers, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Credited= models.FloatField(null=True,blank=True )  # 'deposit' or 'withdraw'
    Debited= models.FloatField(null=True , blank=True)  # 'deposit' or 'withdraw'
    Transferred= models.CharField(max_length=40 ,blank=True,null=True)  # 'deposit' or 'withdraw'
    date_field = models.DateField(auto_now=True)
    time_field = models.TimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username}'s Account"
    


    def save(self, *args, **kwargs):
        # Update the current_balance of the associated BankUser
         
        if self.bank_user:
            self.bank_user.current_balance += self.Credited/2 or 0  #here something was going wrong that's why divided by 2 was used here
            self.bank_user.current_balance -= self.Debited/2 or 0
            self.bank_user.save()
        super().save(*args, **kwargs)