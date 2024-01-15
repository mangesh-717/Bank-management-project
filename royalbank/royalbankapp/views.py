from django.shortcuts import render,redirect
from .models import Bankusers,CardApplication,LoanRequest,Transaction
from django.contrib.auth.models import User
from .forms import loginform,LoanRequestForm,HelpDesk
from django.core.mail import send_mail
from django.utils import timezone
from django.http import HttpResponse

subject = 'Amount Transferred'
transaction_time = timezone.now()
formatted_time = transaction_time.strftime('%Y-%m-%d %H:%M:%S')  # Format the timestamp as per your preference


# Create your views here.
def home(request):


    from django.urls import reverse

    if request.method == 'POST':
            username = request.POST.get('searching')
            try:
                username = request.POST.get('searching')
                user=User.objects.get(username=username)
                acc=Bankusers.objects.get(id=user.id)
                home_url = reverse('home')  # Replace 'home' with your actual URL name

                # return HttpResponse(f'<body style="background-color: black; color: white;"><h2>{user.first_name} Your AccountNumber is: {acc.account_number}</h2></body>')
                return HttpResponse(f'''
                <body style="background-color: black; color: white;">
                    <h3>{user.first_name} Your AccountNumber is: {acc.account_number}</h3>
<button style="background-color: #312b5a; color: rgb(198, 193, 193); padding: 10px; border: none; cursor: pointer; border-radius: 5px;" onclick="window.location.href='{home_url}'">Go to Home</button>

                </body>
            ''')
            except User.DoesNotExist:
                return HttpResponse(f'<body style="background-color: black; color: red;"> <h2>User not found</h2></body>')
            except Bankusers.DoesNotExist:
                return HttpResponse(f'<body style="background-color: black; color: White;"> <h2>Account number not found</h2></body>')
    
    return render(request,'home.html')

from .models import Bankusers
from django.contrib.auth.models import User
from django.contrib import messages
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        username=request.POST['username']
        password=request.POST['password']
        account_type=request.POST['account-type']
        adhar_card=request.FILES['aadhar-card']
        photo=request.FILES['photo']
        if User.objects.filter(username=username):
            messages.error(request,'⚠️ username already exists go for login')
            print('problem')
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, first_name=name, last_name=lastname)
        user.set_password(password)
        bank_user = Bankusers.objects.create(
            account_type=account_type,
            phon=phone,
            photo=photo,
            adhar=adhar_card
        )
        bank_user.save()
        user.save()
        messages.success(request,'user has been succesfully created \n login now')
        try:
            userid=User.objects.get(username=username)
            user_account = Bankusers.objects.get(id=userid.id)
        # print(user_account.account_number)
            subject = 'Registration Successful - Welcome to Royal Bank!'
            message = f'Congratulations {name},\n\n' \
                      f'Your registration with Royal Bank has been successfully completed.\n' \
                      f'Account Number: {user_account.account_number}\n\n' \
                       f'Thank you for choosing Royal Bank!\n' \
                       f'Best regards,\n' \
                       f'Royal Bank'
        
            from_email = 'mangeshsathe1353@gmail.com'
            recipient_list = [userid.email]
        
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            messages.error(request, 'An error occurred while processing the registration. Please try again later.')
        
    return render(request,'register.html')






from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def login_form(request):
    use=None
    form=loginform(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            username= form.cleaned_data['username']
            email= form.cleaned_data['Email']
            password = form.cleaned_data['password']
            if not(User.objects.filter(username=username).exists()):
                messages.error(request,"!!.⚠️username does't match")
            else:
                use=authenticate(username=username,password=password)
            if use is None:
                messages.error(request,"⚠️!Invalid Password")
                return redirect("loginform")
            else:
                login(request,use)
                request.session['logged_in_once'] = True  # Set session variable
                messages.success(request, 'Logged in successfully! \n Now you can to your Section')
    form=loginform()
    return render(request,'login.html',{'form':form})

def help(request):
    if request.method == 'POST':
        form = HelpDesk(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Issue has been submitted successfully!')
    form=HelpDesk()
    return render(request,'help.html',{'form':form})



def creadit_debit(request):
    return render(request,'creadit_debit.html')

# from .forms import CardApplicationForm  # Import your form class here
from django.contrib import messages
@login_required(login_url='loginform')
def creadit_debit_form(request):
    if request.method == 'POST':
        user = request.user
        email=request.POST['email']
        debit_card = 'debit' in request.POST
        credit_card ='credit' in request.POST

        if user.email==email:
            # return redirect('home')  # Redirect to the dashboard or any other page
            if CardApplication.objects.filter(user=user).exists():
                if CardApplication.objects.filter(user=user, creaditcard=True).exists() and CardApplication.objects.filter(user=user, debitcard=True).exists():
                    messages.error(request, 'You have already applied for Both cards. Go to Help Section')
                    # return redirect('help')
                else:
                    card_application = CardApplication.objects.get(user=user)
                    if card_application.debitcard==False and debit_card==True:
                        card_application.debitcard = debit_card
                        card_application.save()
                        try:
                            card_type = 'Debit Card'  # Replace with 'Debit Card' if applicable
                            subject = f'{card_type} Application Submitted Successfully'
                            message = f'Dear {user.first_name},\n\n' \
                                      f'Your {card_type} application has been successfully submitted. Our team will review your application and get back to you soon.\n\n' \
                                      f'Transaction Time: {formatted_time}\n\n' \
                                      f'Thank you for choosing Royal Bank!\n' \
                                      f'Best regards,\n' \
                                      f'Royal Bank'
                        
                            from_email = 'mangeshsathe1353@gmail.com'
                            recipient_list = [user.email]
                        
                            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                        except Exception as e:
                            messages.error(request, f'An error occurred while processing the {card_type} application submission. Please try again later.')
                        

                        messages.success(request, 'debit Card application submitted successfully!')
                    if card_application.creaditcard==False and credit_card==True:
                        card_application.creaditcard = credit_card
                        card_application.save()
                        messages.success(request, 'Credit Card application submitted successfully!')
                        try:
                            card_type = 'Credit Card'  # Replace with 'Debit Card' if applicable
                            subject = f'{card_type} Application Submitted Successfully'
                            message = f'Dear {user.first_name},\n\n' \
                                      f'Your {card_type} application has been successfully submitted. Our team will review your application and get back to you soon.\n\n' \
                                      f'Transaction Time: {formatted_time}\n\n' \
                                      f'Thank you for choosing Royal Bank!\n' \
                                      f'Best regards,\n' \
                                      f'Royal Bank'
                        
                            from_email = 'mangeshsathe1353@gmail.com'
                            recipient_list = [user.email]
                        
                            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                        except Exception as e:
                            messages.error(request, f'An error occurred while processing the {card_type} application submission. Please try again later.')
                        

                    if card_application.debitcard==True and debit_card==True or card_application.creaditcard==True and credit_card==True:
                        if debit_card:
                            messages.error(request, '⚠️You have already applied for a debit card.')
                        if credit_card:
                            messages.error(request, '⚠️You have already applied for a credit card.')
    
            else:
                card_application = CardApplication.objects.create(
                user=user,
                creaditcard=credit_card,
                debitcard=debit_card
              )
                card_application.save()
                messages.success(request, 'Card application submitted successfully!')
        else:
            messages.error(request, "⚠️Enter email correctly")
    return render(request,'creadit_form.html')

@login_required(login_url='loginform')
def loan_request_view(request):
    if 'Username' in request.POST:
        print('its loan request')
        user = request.user
        form = LoanRequestForm(request.POST)
        if form.is_valid():
            username= form.cleaned_data['Username']
            email= form.cleaned_data['email']
            amount = form.cleaned_data['amount']
            Loan_Tenure= form.cleaned_data['Loan_Tenure']
            purpose = form.cleaned_data['purpose']
            message = form.cleaned_data['message']
        if LoanRequest.objects.filter(user=user).exists():
            messages.error(request, 'You have already applied for Loan So go to help desk')
        else:
            if user.email==email and user.username==username:
                loan_application= LoanRequest.objects.create(
                        user=user,
                        amount=amount,
                        Loan_Tenure=Loan_Tenure,
                        purpose=purpose,
                        message=message
                      )
                loan_application.save()
                messages.success(request, 'Loan application submitted successfully!')
                try:
                    subject = 'Loan Application Submitted Successfully'
                    message = f'Dear {user.first_name},\n\n' \
                                  f'Your loan application has been successfully submitted. Our team will review your application and get back to you soon.\n\n' \
                                  f'Transaction Time: {formatted_time}\n\n' \
                                  f'Thank you for choosing Royal Bank!\n' \
                                  f'Best regards,\n' \
                                  f'Royal Bank'
                    
                    from_email = 'mangeshsathe1353@gmail.com'
                    recipient_list = [user.email]
                    
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception as e:
                    messages.error(request, 'An error occurred while processing the loan application submission. Please try again later.')

    
            else:
                messages.error(request, "⚠️Enter username and email correctly")
    else:
        form = LoanRequestForm()

        # payed loan amount
    if 'debitAmount' in request.POST:
        print('loan payed')
        user=request.user
        user_account = Bankusers.objects.get(id=user.id)
        if user_account.loan_amount:
            if user_account.current_balance >= user_account.loan_amount:    
                transaction = Transaction.objects.create(
                    user=user,
                    bank_user=user_account,
                    Credited=00,
                    Debited=user_account.loan_amount,    
                    Transferred='debited loan amount',  
                            )  
                transaction.save()                        
                messages.success(request, 'Congratulations You have successfully Payed Your Whole loan Amount!!')
                try:
                    subject = 'Loan Repayment Successful'
                    message = f'Dear {user.first_name},\n\n' \
                              f'Congratulations! You have successfully repaid your entire loan.\n\n' \
                              f'Transaction details:\n' \
                              f'Repaid Amount: {user_account.loan_amount} dollars\n' \
                              f'Transaction Time: {formatted_time}\n\n' \
                              f'Thank you for fulfilling your loan commitment!\n' \
                              f'Best regards,\n' \
                              f'Royal Bank'
                
                    from_email = 'mangeshsathe1353@gmail.com'
                    recipient_list = [user.email]
                
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception as e:
                    messages.error(request, 'An error occurred while processing the loan repayment. Please try again later.')

            else:
                messages.error(request, '⚠️Inefficient Balance !')
        else:
            messages.error(request, "You don't have any Loan!")

    return render(request,'loan.html', {'form': form})


@login_required(login_url='loginform')
def account(request):
    user=request.user
    try:   
        name=user.first_name
        bank_user = Bankusers.objects.get(id=user.id)
        balance=bank_user.current_balance
    except:
        pass

    if 'creditAmount'in request.POST:  
        credit_amount=request.POST.get('creditAmount')
        print(credit_amount)
        try:
            if float(credit_amount)>0:
                transaction = Transaction.objects.create(
                        user=user,
                        bank_user=bank_user,
                        Credited=float(credit_amount),
                        Debited=00.0,    
                        Transferred='Creadeted by Itself',  
                    )
                transaction.save()
                messages.success(request, 'Balance has been successfully Credited!')
                try:
                    subject = 'Balance Credited Successful'
                    message = f'Dear {user.first_name},\n\n' \
                              f'Your balance credit request has been successfully processed.\n\n' \
                              f'Transaction details:\n' \
                              f'credit Balance: {credit_amount} dollars\n' \
                              f'Transaction Time: {formatted_time}\n\n' \
                              f'Thank you for using our service!\n' \
                              f'Best regards,\n' \
                              f'Royal Bank'
                
                    from_email = 'mangeshsathe1353@gmail.com'
                    recipient_list = [user.email]
                
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                except Exception as e:
                    messages.error(request, 'An error occurred while processing the balance retrieval. Please try again later.')
                
            # here mail updatets should be given

        except:
            messages.error(request, "Enter amount correctly.")

    if 'debitAmount' in request.POST:
        debit_amount = request.POST.get('debitAmount')
        try:
            if float(debit_amount)>0:
                user_account = Bankusers.objects.get(id=user.id)
                if user_account.current_balance > float(debit_amount):    
                    transaction = Transaction.objects.create(
                            user=user,
                            bank_user=bank_user,
                            Credited=00,
                            Debited=float(debit_amount),    
                            Transferred='debited by Itself',  
                        )
                    transaction.save()
                    messages.success(request, 'Balance has been successfully Debited!')
# ******************email updates*************
                    try:
                        subject = 'Balance Retrieval Successful'
                        message = f'Dear {user.first_name},\n\n' \
                                  f'Your balance retrieval request has been successfully processed.\n\n' \
                                  f'Transaction details:\n' \
                                  f'Retrieved Balance: {debit_amount} dollars\n' \
                                  f'Transaction Time: {formatted_time}\n\n' \
                                  f'Thank you for using our service!\n' \
                                  f'Best regards,\n' \
                                  f'Royal Bank'
                    
                        from_email = 'mangeshsathe1353@gmail.com'
                        recipient_list = [user.email]
                    
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    except Exception as e:
                        messages.error(request, 'An error occurred while processing the balance retrieval. Please try again later.')

                        
                else:
                    messages.error(request,'Entered debit amount is greater than your current balance')
        except:
            messages.error(request, "Enter amount correctly.")


    if 'Emipayed' in request.POST:
        if Bankusers.objects.get(id=user.id).loan_amount:
            loan=Bankusers.objects.get(id=user.id)
            loan.loan_amount=-loan.emi
            loan.save()

            updationTransactions=Transaction.objects.create(
                            user=user,
                            bank_user=bank_user,
                            Credited=00,
                            Debited=float(Bankusers.objects.get(id=user.id).emi),    
                            Transferred='debited Emi',    
                        )
            updationTransactions.save()
            messages.success(request, 'Emi has been successfully Paied!')
            try:
                subject = 'EMI Successfully Submitted'
                message = f'Dear {user.first_name},\n\n' \
                          f'Your EMI payment of {float(Bankusers.objects.get(id=user.id).emi)} dollars has been successfully completed.\n\n' \
                          f'Transaction details:\n' \
                          f'EMI Amount: {float(Bankusers.objects.get(id=user.id).emi)}\n' \
                          f'Transaction Time: {formatted_time}\n\n' \
                          f'Thank you for using our service!\n' \
                          f'Best regards,\n' \
                          f'Royal Bank'
            
                from_email = 'mangeshsathe1353@gmail.com'
                recipient_list = [user.email]
            
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                messages.error(request, 'An error occurred while processing the EMI payment. Please try again later.')
            

        else:
            messages.error(request, "You Don't have any Loan.")

            

    if 'transferAmount' in request.POST:
        transferAmount=request.POST.get('transferAmount')
        recipientemail=request.POST.get('recipientEmail')
        recipientAccountNo=request.POST.get('recipientAccount')
        


        # print(credit_amount,debit_amount,transferAmount,recipientAccountNo,recipientemail)
        from django.core.exceptions import ObjectDoesNotExist
        try:
            user=request.user
            user_account = Bankusers.objects.get(id=user.id)
            senderbalance=user_account.current_balance
            recipientAccountnumber=int(recipientAccountNo)
            transferAmoun=float(transferAmount)
            user_account.save()
            if senderbalance>=transferAmoun:
                if Bankusers.objects.get(account_number=recipientAccountnumber).id == User.objects.get(email=recipientemail).id and user.email != recipientemail :
                    
                    
                    # and this is associeated with history
                    # here we have added transfered amount to specified user
                    reciveruserr=User.objects.get(email=recipientemail)
                    recipientemailuser = Bankusers.objects.get(account_number=recipientAccountnumber) 
                    
                    recipienthistory=Transaction.objects.create(
                            user=reciveruserr,
                            bank_user=recipientemailuser,
                            Credited=float(transferAmoun),
                            Debited=00,    
                            Transferred=f'Recived from {user.email}' ,    
                        )
                    recipienthistory.save() 
                    #here we need to update reciver updates by email

                    try:
                        subject = 'Amount Received'            
                        message = f'Dear {reciveruserr},\n\n' \
                                  f'You have successfully Received {transferAmoun} dollar  from {user.email}.\n\n' \
                                  f'Transaction details:\n' \
                                  f'Received Amount: {transferAmoun}\n' \
                                  f'Sender Email: {user.email}\n' \
                                  f'Transaction Time: {formatted_time}\n\n' \
                                  f'Thank you for using our service!\n' \
                                  f'Best regards,\n' \
                                  f'Royal bank'
                        from_email = 'mangeshsathe1353@gmail.com'  
                        recipient_list = [recipientemail]
                
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    except:
                        messages.error(request, 'An error occurred while processing the transfer. Please try again later.')

                    
                    # here we have debedeted amount from transferer user  
                    transaction = Transaction.objects.create(
                            user=user,
                            bank_user=bank_user,
                            Credited=00,
                            Debited=float(transferAmoun),    
                            Transferred=f'Transfered by you to {recipientemail}' ,  
                        )
                    transaction.save()  


    #***************** here we have to update sender updates by email      ****************************
                    try:
                        subject = 'Amount Transferred'            
                        message = f'Dear {user.first_name},\n\n' \
                                  f'You have successfully transferred {transferAmoun} dollar  to {recipientemail}.\n\n' \
                                  f'Transaction details:\n' \
                                  f'Transfer Amount: {transferAmoun}\n' \
                                  f'Recipient Email: {recipientemail}\n' \
                                  f'Transaction Time: {formatted_time}\n\n' \
                                  f'Thank you for using our service!\n' \
                                  f'Best regards,\n' \
                                  f'Royal bank'
                        from_email = 'mangeshsathe1353@gmail.com'  
                        recipient_list = [user.email]
                
                        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    except:
                        messages.error(request, 'An error occurred while processing the transfer. Please try again later.')


                    # print('succiedddd')
                    messages.success(request, 'Balance has been successfully Transferred!')

                #    reciver.save()
                else:
                    messages.error(request, "Recipient Account No or Email is Wrong.")

                    # print('something wrongn')
        except Bankusers.DoesNotExist:
            print('error')
        
    
    return render(request,'operations.html',{'name':name , 'dbalance':balance})

def About(request):
    return render(request,'about.html')

def carrier(request):
    return render(request,'join-our-tem.html')

@login_required(login_url='loginform')
def result(request):
    user=request.user
    user_id = request.user.id
    name=request.user.first_name
    if request.method == 'POST':
        try:
            display=int(request.POST.get('num_transactions'))
            target_user_history = Transaction.objects.filter(user_id=user_id).order_by('date_field','-time_field')[:display]
            fo=Transaction.objects.filter(user_id=user_id)
            return render(request,'result.html',{'name':name,'data':target_user_history,})
        except:
            # pass
            print('error')
    return render(request,'result.html',{'name':name})




