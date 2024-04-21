import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .models import Residents, RentalFee, PettyCash,PettyCashType
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

def residents_list(request):
    residents = Residents.objects.all()
    paginator = Paginator(residents, 10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number or 1)
    print(page_obj[0].id)

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
        if rental_fee_id:  # If rental_fee_id exists, it's an edit operation
            rental_fee_instance = get_object_or_404(RentalFee, pk=rental_fee_id)
            form = RentalFeeForm(request.POST, instance=rental_fee_instance)
            if form.is_valid():
                form.save()
                return redirect('resident_detail', id=id)
        else:  # Otherwise, it's a create operation
            form = RentalFeeForm(request.POST)
            if form.is_valid():
                rental_fee = form.save(commit=False)
                rental_fee.resident = resident
                rental_fee.save()
                return redirect('resident_detail', id=id)

        # Handle PettyCash form
        petty_cash_id = request.POST.get('petty_cash_id')
        print(petty_cash_id)
        if petty_cash_id: 
            petty_cash_instance = get_object_or_404(PettyCash, pk=petty_cash_id)
            petty_form = PettyCashForm(request.POST, instance=petty_cash_instance)
            if petty_form.is_valid():
                if petty_cash_instance.type == 'Withdrawl':
                    change = petty_cash_instance.withdrawl - petty_form.withdrawl
                    petty_form.balance = petty_cash_instance.balance + change
                else: 
                    change = petty_cash_instance.deposit - petty_form.deposit
                    petty_form.balance = petty_cash_instance.balance - change

                petty_form.save()
                return redirect('resident_detail', id=id)
        else:  
            petty_form = PettyCashForm(request.POST)
            if petty_form.is_valid():
                petty_cash = petty_form.save(commit=False)
                petty_cash.resident = resident
                if(petty_cash.type == 'Withdrawl'):
                    if (resident.pettycash_set.all().last()):
                        petty_cash.balance = resident.pettycash_set.all().last().balance - petty_cash.withdrawl
                    else:
                        petty_cash.balance = -1* petty_cash.withdrawl
                else: 
                    if (resident.pettycash_set.all().last()):
                        petty_cash.balance = resident.pettycash_set.all().last().balance + petty_cash.deposit
                    else:
                        petty_cash.balance = petty_cash.deposit
                petty_cash.save()
                return redirect('resident_detail', id=id)
        
        # Handle rental fee deletion
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

from django.urls import reverse

def generate_report(request, id):
    startdate_str = request.GET.get('startdate')
    enddate_str = request.GET.get('enddate')
    year_render = request.GET.get('year')
    petty_render = request.GET.get('petty')
    
    startdate = datetime.strptime(startdate_str, '%Y-%m-%d').date() if startdate_str else None
    enddate = datetime.strptime(enddate_str, '%Y-%m-%d').date() if enddate_str else None
    if startdate:
        if year_render:
            url = reverse('generate_yearly_pdf', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
            return redirect(url)
        elif petty_render:
            url = reverse('generate_pdf_petty', kwargs={'id': id, 'startdate': startdate, 'enddate': enddate})
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
    petty_cash_transactions = PettyCash.objects.annotate(month=ExtractMonth('date')).filter(
        Q(date__gte=startdate_obj) & Q(date__lte=enddate_obj),
        resident=resident
    )
    
    deposit_amounts = [transaction.deposit for transaction in petty_cash_transactions if transaction.deposit is not None]
    withdrawal_amounts = [transaction.withdrawl for transaction in petty_cash_transactions if transaction.withdrawl is not None]

    # Calculate the total deposit and withdrawal
    total_deposit = sum(deposit_amounts)
    total_withdrawal = sum(withdrawal_amounts)

    balance = total_deposit - total_withdrawal
    total_amount = sum([fee.amount for fee in rental_fees]) + balance
    twenty_percent = total_amount * decimal.Decimal('0.20')
    sixty_percent = total_amount * decimal.Decimal('0.60')
    twenty_percent_again = total_amount * decimal.Decimal('0.20')

    # Render the PDF with the retrieved data
    template = get_template('yearly_report_template.html')
    context = {
        'resident': resident,
        'date': date,
        'startdate': startdate_obj,
        'enddate': enddate_obj,
        'rental_fees': rental_fees,
        'petty_cash_transactions': petty_cash_transactions,
        'total_amount': total_amount,
        'twenty_percent': twenty_percent,
        'sixty_percent': sixty_percent,
        'twenty_percent_again': twenty_percent_again,
    }
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Yearly_Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

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

    # Calculate the total deposit and withdrawal
    total_deposit = sum(deposit_amounts)
    total_withdrawal = sum(withdrawal_amounts)
    balance = total_deposit - total_withdrawal
    
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
    }
    html = template.render(context)

    # Generate PDF using xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=Report_{startdate_obj.strftime("%Y-%m-%d")}_to_{enddate_obj.strftime("%Y-%m-%d")}.pdf'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def view_my_report(request):
    return render(request, 'yearly_report_template.html')