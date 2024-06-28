import datetime
import os
from django.shortcuts import render, redirect, get_object_or_404
from .models import Residents, RentalFee, PettyCash,PettyCashType,EmailLogs
from .forms import RentalFeeForm, PettyCashForm, ResidentForm
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime
from django.db.models.functions import ExtractMonth
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
import decimal
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
import base64
from django.core.mail import EmailMessage
from email.utils import formataddr
import logging
from django.urls import reverse

logger = logging.getLogger(__name__)

def my_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')  
    
from django.contrib.staticfiles import finders

def fetch_resources(uri, rel):
    if uri.startswith('/static/'):
        path = finders.find(uri[1:])  # Strip leading slash
        if path:
            print(f"Resolved path: {path}")
            return path
    print(f"Unresolved URI: {uri}")
    return uri

def my_logout_view(request):
    logout(request)
    return redirect('login')  

def residents_list(request):
    residents = Residents.objects.all()
    paginator = Paginator(residents, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number or 1)

    return render(request, 'residents_list.html', {'page_obj': page_obj})

def search_residents(request):
    query = request.GET.get('q')
    residents = Residents.objects.all() 

    if query:  
        residents = residents.filter(
            resident_first_name__icontains=query
        ) | residents.filter(
            resident_last_name__icontains=query
        ) | residents.filter(
            room_number__icontains=query
        )

    data = [{'resident_id': resident.id,
             'resident_first_name': resident.resident_first_name,
             'resident_last_name': resident.resident_last_name,
             'contact_name': resident.contact_name,
             'relation1': resident.relation1,
             'phone_number': resident.phone_number,
             'admission_date': resident.admission_date,
             }
            for resident in residents]

    return JsonResponse(data, safe=False)
def resident_detail(request, id):
    resident = get_object_or_404(Residents, id=id)
    petty_cash_types = PettyCashType.objects.all()

    if request.method == 'POST':
        rental_fee_id = request.POST.get('rental_fee_id')
        if rental_fee_id: 
            rental_fee_instance = get_object_or_404(RentalFee, pk=rental_fee_id)
            form = RentalFeeForm(request.POST, instance=rental_fee_instance)
            if form.is_valid():
                form.save()
                return redirect('resident_detail', id=id)
        else: 
            form = RentalFeeForm(request.POST)
            if form.is_valid():
                rental_fee = form.save(commit=False)
                rental_fee.resident = resident
                rental_fee.save()
                return redirect('resident_detail', id=id)

        petty_cash_id = request.POST.get('petty_cash_id')
        print(petty_cash_id)
        #reverse logic for balance like credit card statement
        if petty_cash_id: 
            petty_cash_instance = get_object_or_404(PettyCash, pk=petty_cash_id)
            old_withdrawl = petty_cash_instance.withdrawl
            old_deposit = petty_cash_instance.deposit
            old_balance = petty_cash_instance.balance
            old_petty_cash_type = petty_cash_instance.petty_cash_type
            petty_form = PettyCashForm(request.POST, instance=petty_cash_instance)
            if petty_form.is_valid():
                petty_form = petty_form.save(commit=False)
                print(petty_form)
                if petty_cash_instance.type == 'Withdrawl':
                    change = old_withdrawl - petty_form.withdrawl
                    print('change --> ' + str(change))
                    petty_form.balance = old_balance - change
                else: 
                    change = old_deposit - petty_form.deposit
                    petty_form.balance = old_balance + change

                petty_form.save()
                return redirect('resident_detail', id=id)
        else:  
            petty_form = PettyCashForm(request.POST)
            if petty_form.is_valid():
                petty_cash = petty_form.save(commit=False)
                petty_cash.resident = resident
                if(petty_cash.type == 'Withdrawl'):
                    if (resident.pettycash_set.all().last()):
                        petty_cash.balance = resident.pettycash_set.all().last().balance + petty_cash.withdrawl
                    else:
                        petty_cash.balance = 1* petty_cash.withdrawl
                else: 
                    if (resident.pettycash_set.all().last()):
                        petty_cash.balance = resident.pettycash_set.all().last().balance - petty_cash.deposit
                    else:
                        petty_cash.balance = -1*petty_cash.deposit
                petty_cash.save()
                return redirect('resident_detail', id=id)
        
        fee_id = request.POST.get('delete_rental_fee_id')
        if fee_id:
            fee = get_object_or_404(RentalFee, pk=fee_id)
            fee.delete()
            messages.success(request, 'Rental Fee record deleted successfully.')
            return redirect('resident_detail', id=id)
        
        petty_cash_id_delete = request.POST.get('petty_cash_id_delete')
        if petty_cash_id_delete:
            petty = get_object_or_404(PettyCash, pk=petty_cash_id_delete)
            petty.delete()
            messages.success(request, 'Petty Cash record deleted successfully.')
            return redirect('resident_detail', id=id)

    else:
        form = RentalFeeForm()
        petty_form = PettyCashForm()

    return render(request, 'resident_detail.html', {'form': form, 'petty_form': petty_form, 'resident': resident, 'petty_cash_types': petty_cash_types})


def add_resident(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('residents_list')  
    else:
        form = ResidentForm()
    return render(request, 'add_resident.html', {'form': form})

def email_logs(request):
    return redirect('/admin/seniorApp/emaillogs/')

def edit_resident(request, id):
    resident = get_object_or_404(Residents, id=id)
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            return redirect('residents_list')
    else:
        form = ResidentForm(instance=resident)
    return render(request, 'edit_resident.html', {'form': form})

def generate_report(request, id):
    startdate_str = request.GET.get('startdate')
    enddate_str = request.GET.get('enddate')
    year_render = request.GET.get('year')
    petty_render = request.GET.get('petty')
    send_email_yearly = request.GET.get('sendemail_yearly')
    send_email_Petty = request.GET.get('sendemail_Petty')
    print(send_email_Petty)
    send_email_Rental = request.GET.get('sendemail_Rental')
    
    startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date() if startdate_str else None
    enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date() if enddate_str else None
    if startdate:
        if year_render:
            url = reverse('generate_yearly_pdf', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        elif petty_render:
            url = reverse('generate_pdf_petty', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        elif send_email_yearly:
            url = reverse('sendemail_yearly', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        elif send_email_Petty:
            url = reverse('sendemail_pdf_petty', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        elif send_email_Rental:
            url = reverse('sendemail_pdf_rental', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        else:
            url = reverse('generate_pdf', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
    else:
        return HttpResponse("Please provide a valid date parameter.")
    

def generate_yearly_pdf(request, id, startdate,enddate):
    date = datetime.today().date()
    startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
    enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
    resident = get_object_or_404(Residents, id=id)
    rental_fees = RentalFee.objects.filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    total_amount = sum([fee.amount for fee in rental_fees]) 
    twenty_percent = total_amount * decimal.Decimal('0.20')
    sixty_percent = total_amount * decimal.Decimal('0.60')
    twenty_percent_again = total_amount * decimal.Decimal('0.20')
    template = get_template('yearly_report_template.html')
    context = {
        'resident': resident,
        'date': date,
        'startdate': startdate_obj,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'total_amount': total_amount,
        'twenty_percent': twenty_percent,
        'sixty_percent': sixty_percent,
        'twenty_percent_again': twenty_percent_again,
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Yearly_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8', link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_pdf(request, id, startdate,enddate):
    date = datetime.today().date()
    startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
    enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
    resident = get_object_or_404(Residents, id=id)
    rental_fees = RentalFee.objects.filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    petty_cash_transactions = PettyCash.objects.annotate(month=ExtractMonth('date')).filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    total_amount = total_amount = sum([fee.amount for fee in rental_fees])
    all_paid = all(fee.paid for fee in rental_fees)
    template = get_template('rental_report.html')
    context = {
        'resident': resident,
        'date': date,
        'startdate': startdate_obj,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'petty_cash_transactions': petty_cash_transactions,
        'total_amount': total_amount,
        'all_paid': all_paid,
    }
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Rental_Fee_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8', link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_pdf_petty(request, id, startdate,enddate):
    startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
    date = datetime.today().date()
    enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
    resident = get_object_or_404(Residents, id=id)
    rental_fees = RentalFee.objects.filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    petty_cash_transactions = PettyCash.objects.annotate(month=ExtractMonth('date')).filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    total_amount = sum([fee.amount for fee in rental_fees]) + sum([transaction.deposit for transaction in petty_cash_transactions])
    deposit_amounts = [transaction.deposit for transaction in petty_cash_transactions if transaction.deposit is not None]
    withdrawal_amounts = [transaction.withdrawl for transaction in petty_cash_transactions if transaction.withdrawl is not None]
    total_deposit = sum(deposit_amounts)
    total_withdrawal = sum(withdrawal_amounts)
    balance = total_deposit - total_withdrawal
    if len(petty_cash_transactions) > 0:
        balance = petty_cash_transactions.last().balance
    # if balance >= 0:
    #     balance = 0
    # else:
    #     balance = abs(balance)
    print('Balance --> ' + str(balance))
    closest_previous_balance = PettyCash.objects.filter(date__lt=startdate_obj, resident=resident).order_by('-date').first()
    if closest_previous_balance:
        closest_previous_balance = closest_previous_balance.balance

        
    
    # Render the PDF with the retrieved data
    template = get_template('petty_cash_report.html')
    context = {
        'resident': resident,
        'startdate': startdate_obj,
        'date': date,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'petty_cash_transactions': petty_cash_transactions,
        'total_amount': total_amount,
        'balance': balance,
        'closest_previous_balance': closest_previous_balance,
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Petty_Cash_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8', link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def sendemail_yearly(request, id, startdate, enddate):
    try:
        date = datetime.today().date()
        startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
        enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
        resident = get_object_or_404(Residents, id=id)

        rental_fees = RentalFee.objects.filter(
            Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
            resident=resident
        )

        total_amount = sum([fee.amount for fee in rental_fees]) 
        twenty_percent = total_amount * decimal.Decimal('0.20')
        sixty_percent = total_amount * decimal.Decimal('0.60')
        twenty_percent_again = total_amount * decimal.Decimal('0.20')

        template = get_template('yearly_report_template.html')
        context = {
            'resident': resident,
            'date': date,
            'startdate': startdate_obj,
            'enddate': enddate_obj,
            'rental_fees': rental_fees,
            'total_amount': total_amount,
            'twenty_percent': twenty_percent,
            'sixty_percent': sixty_percent,
            'twenty_percent_again': twenty_percent_again,
        }
        html = template.render(context)

        pdf_content = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_content, encoding='utf-8', link_callback=fetch_resources)

        if pisa_status.err:
            logger.error('Error rendering PDF: %s', html)
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        pdf_content.seek(0)
        subject = 'Yearly Report PDF'
        message = f"""
        <html>
        <body>
            <p>Dear {resident.contact_name},</p>

            <p>I hope you're doing well. Attached is the Yearly Report PDF for services provided at L'chaim Retirement Home. Kindly send an e-transfer to payments@lchaimretirement.ca.</p>

            <p>Warmest Regards,</p><br>

            <p style="font-size: 14px; color: #808080;">
                <h3 style="color: #808080;">L'chaim Retirement Home</h3>
                <h3>Deborah Rothenberg - Director of Operations</h3>
                <p>P. 416-398-7898 Ext. 222</p>
                <p>E. deborah@lchaimretirement.ca</p>
                <p>W. <a href="http://www.lchaimretirement.ca" style="color: #808080;">www.lchaimretirement.ca</a></p>
            </p>
            <br/>
            <p>
                <h3 style="font-style: italic; color: #333; font-family: 'Times New Roman', Times, serif;">
                    The Right Choice For Quality Living
                </h3>
                <p style="font-size:12px; font-style: italic; color: #333;"><i>This message is confidential and may be privileged. If you are not the intended recipient, please notify me and permanently delete this message and any attachments without reading it or making a copy. </p>
            </p>
        </body>
        </html>
        """

        email_from = settings.EMAIL_HOST_USER

        if not resident.email_address:
            logger.warning('Email Address Not Present in Resident Info for resident id %s', resident.id)
            return HttpResponse('Email Address Not Present in Resident Info')

        recipient_list = [resident.email_address]
        email = EmailMessage(
            subject,
            message,
            from_email='L\'chaim Retirement Homes <lcahim@app.lchaimretirement.ca>',
            to=recipient_list,
            reply_to=['deborah@lchaimretirement.ca']
        )
        email.content_subtype = "html"  # Set the content subtype to HTML

        email.attach(
            f'Yearly_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
            pdf_content.getvalue(),
            'application/pdf'
        )

        email.send()

        email_log = EmailLogs(
            resident_name=f"{resident.resident_first_name} {resident.resident_last_name}",
            emailed_report_name=f'Yearly Report {startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
            email_body=message,
            resident=resident,
            date=date
        )
        email_log.save()

        resident_name=f"{resident.resident_first_name} {resident.resident_last_name}"
        return render(request, 'email_sent_success.html', {'resident_name': resident_name})

    except Exception as e:
        logger.error('Error in sending yearly email: %s', str(e), exc_info=True)
        return HttpResponse('An error occurred while sending the email. Please try again later.', status=500)

def sendemail_pdf_petty(request, id, startdate,enddate):
    startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
    date = datetime.today().date()
    enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
    resident = get_object_or_404(Residents, id=id)
    rental_fees = RentalFee.objects.filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    petty_cash_transactions = PettyCash.objects.annotate(month=ExtractMonth('date')).filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    total_amount = sum([fee.amount for fee in rental_fees]) + sum([transaction.deposit for transaction in petty_cash_transactions])
    deposit_amounts = [transaction.deposit for transaction in petty_cash_transactions if transaction.deposit is not None]
    withdrawal_amounts = [transaction.withdrawl for transaction in petty_cash_transactions if transaction.withdrawl is not None]
    total_deposit = sum(deposit_amounts)
    total_withdrawal = sum(withdrawal_amounts)
    balance = total_deposit - total_withdrawal
    if len(petty_cash_transactions) > 0:
        balance = petty_cash_transactions.last().balance
    # if balance >= 0:
    #     balance = 0
    # else:
    #     balance = abs(balance)
    print('Balance --> ' + str(balance))
    closest_previous_balance = PettyCash.objects.filter(date__lt=startdate_obj, resident=resident).order_by('-date').first()
    if closest_previous_balance:
        closest_previous_balance = closest_previous_balance.balance

    template = get_template('petty_cash_report.html')
    context = {
        'resident': resident,
        'startdate': startdate_obj,
        'date': date,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'petty_cash_transactions': petty_cash_transactions,
        'total_amount': total_amount,
        'balance': balance,
        'closest_previous_balance': closest_previous_balance,
    }
    html = template.render(context)

    pdf_content = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_content, encoding='utf-8', link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    pdf_content.seek(0)
    
    subject = 'Petty Cash Report'
    message = f"""
        <html>
        <body>
            <p>Dear {resident.resident_first_name},</p>

            <p>I hope you're doing well. Attached is the Yearly Report PDF for services provided at L'chaim Retirement Home. Kindly send an e-transfer to payments@lchaimretirement.ca.</p>

            <p>Warmest Regards,</p><br>

            <p style="font-size: 14px; color: #808080;">
                <h3 style="color: #808080;">L'chaim Retirement Home</h3>
                <h3>Deborah Rothenberg - Director of Operations</h3>
                <p>P. 416-398-7898 Ext. 222</p>
                <p>E. deborah@lchaimretirement.ca</p>
                <p>W. <a href="http://www.lchaimretirement.ca" style="color: #808080;">www.lchaimretirement.ca</a></p>
            </p>
             <br/>
            <p>
                <h3 style="font-style: italic; color: #333; font-family: 'Times New Roman', Times, serif;">
                    The Right Choice For Quality Living
                </h3>
                <p style="font-size:12px; font-style: italic; color: #333;"><i>This message is confidential and may be privileged. If you are not the intended recipient, please notify me and permanently delete this message and any attachments without reading it or making a copy. </p>
            </p>
        </body>
        </html>
        """
    email_from = settings.EMAIL_HOST_USER

    if resident.email_address:
        recipient_list = [resident.email_address]
    else: 
        logger.warning('Email Address Not Present in Resident Info for resident id %s', resident.id)
        return HttpResponse('Email Address Not Present in Resident Info')

    email = EmailMessage(
        subject,
        message,
        from_email='L\'chaim Retirement Homes <lcahim@app.lchaimretirement.ca>',
        to=recipient_list,
        reply_to=['deborah@lchaimretirement.ca']
    )
    email.content_subtype = "html"  # Set the content subtype to HTML

    email.attach(
        f'Petty_Cash_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
        pdf_content.getvalue(),
        'application/pdf'
    )

    email.send()
    
    email_log = EmailLogs(
        resident_name=f"{resident.resident_first_name} {resident.resident_last_name}",
        emailed_report_name=f'Petty Cash Report {startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
        email_body=message,
        resident=resident,
        date=date
    )
    email_log.save()
    resident_name=f"{resident.resident_first_name} {resident.resident_last_name}"
    return render(request, 'email_sent_success.html', {'resident_name': resident_name})

def sendemail_pdf_rental(request, id, startdate,enddate):
    date = datetime.today().date()
    startdate_obj = datetime.strptime(startdate, '%Y-%m-%d').date()
    enddate_obj = datetime.strptime(enddate, '%Y-%m-%d').date()
    resident = get_object_or_404(Residents, id=id)
    rental_fees = RentalFee.objects.filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    petty_cash_transactions = PettyCash.objects.annotate(month=ExtractMonth('date')).filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    total_amount = total_amount = sum([fee.amount for fee in rental_fees])
    
    # Render the PDF with the retrieved data
    template = get_template('rental_report.html')
    context = {
        'resident': resident,
        'date': date,
        'startdate': startdate_obj,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'petty_cash_transactions': petty_cash_transactions,
        'total_amount': total_amount,
    }
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    pdf_content = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_content, encoding='utf-8', link_callback=fetch_resources)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    pdf_content.seek(0)
    
    subject = 'L\'chaim Monthly Invoice'
    message = f"""
        <html>
        <body>
            <p>Dear {resident.contact_name},</p>

            <p>I hope you're doing well. Please see the attached paid monthly invoice.</p>

            <p>All the best</p><br>

            <p style="font-size: 14px; color: #808080;">
                <h3 style="color: #808080;">L'chaim Retirement Home</h3>
                <h3>Deborah Rothenberg - Director of Operations</h3>
                <p>P. 416-398-7898 Ext. 222</p>
                <p>E. deborah@lchaimretirement.ca</p>
                <p>W. <a href="http://www.lchaimretirement.ca" style="color: #808080;">www.lchaimretirement.ca</a></p>
            </p>
             <br/>
            <p>
                <h3 style="font-style: italic; color: #333; font-family: 'Times New Roman', Times, serif;">
                    The Right Choice For Quality Living
                </h3>
                <p style=" font-size:10px; font-style: italic; color: #333;"><i>This message is confidential and may be privileged. If you are not the intended recipient, please notify me and permanently delete this message and any attachments without reading it or making a copy. </p>
            </p>
        </body>
        </html>
        """

    email_from = formataddr(("L'chaim Retirement Home", settings.EMAIL_HOST_USER))

    if resident.email_address:
        recipient_list = [resident.email_address]
    else:
        logger.warning('Email Address Not Present in Resident Info for resident id %s', resident.id)
        return HttpResponse('Email Address Not Present in Resident Info')

    email = EmailMessage(
        subject,
        message,
        from_email='L\'chaim Retirement Homes <lcahim@app.lchaimretirement.ca>',
        to=recipient_list,
        reply_to=['deborah@lchaimretirement.ca']
    )
    email.content_subtype = "html"  # Set the content subtype to HTML

    email.attach(
        f'Rental_Fee_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
        pdf_content.getvalue(),
        'application/pdf'
    )

    email.send()

    email_log = EmailLogs(
        resident_name=f"{resident.resident_first_name} {resident.resident_last_name}",
        emailed_report_name=f'Rental Fee Report {startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf',
        email_body=message,
        resident=resident,
        date=date
    )
    email_log.save()

    resident_name=f"{resident.resident_first_name} {resident.resident_last_name}"
    return render(request, 'email_sent_success.html', {'resident_name': resident_name})


def view_my_report(request):
    return render(request, 'petty_cash_report.html')