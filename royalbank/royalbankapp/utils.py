from django.core.mail import send_mail,EmailMessage
# from django.Http import HttpResponse
# Your view or function
def send_email_v(request):
    subject = 'Subject of the email'
    message = 'this message was sent by django.'
    from_email = 'mangeshsathe1353@gmail.com'  # Sender's email address
    recipient_list = ['mangeshsathe2003@gmail.com']  # Recipient's email address

    send_mail(subject, message, from_email, recipient_list)
send_email_v()
    # Optionally, you can redirect to a success page or return a response
    # return HttpResponse ('Email sent successfully!')
    


# utils.py
# from django.core.mail import send_mail
# from django.http import HttpResponse

# def send_balance_credit_update(email, amount):
#     subject = 'Balance Credited'
#     message = f'Your account has been credited successfully with {amount} units.'
#     send_mail(subject, message, 'your_bank_email@example.com', [email])
#     return HttpResponse('Balance update email sent successfully!')

# def send_balance_debit_update(email, amount):
#     subject = 'Balance Debited'
#     message = f'Your account has been debited successfully with {amount} units.'
#     send_mail(subject, message, 'your_bank_email@example.com', [email])
#     return HttpResponse('Balance update email sent successfully!')

# def send_loan_application_update(email):
#     subject = 'Loan Application Submitted'
#     message = 'Your loan application has been successfully submitted. We will review it and notify you soon.'
#     send_mail(subject, message, 'your_bank_email@example.com', [email])
#     return HttpResponse('Loan application update email sent successfully!')

# def send_credit_card_application_update(email):
#     subject = 'Credit Card Application Submitted'
#     message = 'Your credit card application has been successfully submitted. We will review it and notify you soon.'
#     send_mail(subject, message, 'your_bank_email@example.com', [email])
#     return HttpResponse('Credit card application update email sent successfully!')

# def send_amount_transfer_update(sender_email, receiver_email, amount):
#     subject = 'Amount Transferred'
#     message = f'You have successfully transferred {amount} units to {receiver_email}.'
#     send_mail(subject, message, 'your_bank_email@example.com', [sender_email])
#     return HttpResponse('Amount transfer update email sent successfully!')

# def send_balance_credited_by_someone_update(email, amount, sender_name):
#     subject = 'Balance Credited'
#     message = f'Your account has been credited with {amount} units by {sender_name}.'
#     send_mail(subject, message, 'your_bank_email@example.com', [email])
#     return HttpResponse('Balance update email sent successfully!')




# from .utils import send_email_v






