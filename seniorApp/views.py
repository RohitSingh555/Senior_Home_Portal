from django.shortcuts import render, redirect, get_object_or_404
from .models import Residents, RentalFee, PettyCash,PettyCashType
from .forms import RentalFeeForm, PettyCashForm, ResidentForm
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from reportlab.lib import colors # type: ignore
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle # type: ignore
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle # type: ignore
from reportlab.lib.units import inch # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from datetime import date
def residents_list(request):
    residents = Residents.objects.all()
    return render(request, 'residents_list.html', {'residents': residents})

def resident_detail(request, resident_id):
    resident = get_object_or_404(Residents, resident_id=resident_id)
    petty_cash_types = PettyCashType.objects.all()

    if request.method == 'POST':
        rental_fee_id = request.POST.get('rental_fee_id')
        print(rental_fee_id)
        if rental_fee_id:  # If rental_fee_id exists, it's an edit operation
            rental_fee_instance = get_object_or_404(RentalFee, pk=rental_fee_id)
            form = RentalFeeForm(request.POST, instance=rental_fee_instance)
            if form.is_valid():
                form.save()
                return redirect('resident_detail', resident_id=resident_id)
        else:  # Otherwise, it's a create operation
            form = RentalFeeForm(request.POST)
            if form.is_valid():
                rental_fee = form.save(commit=False)
                rental_fee.resident = resident
                rental_fee.save()
                return redirect('resident_detail', resident_id=resident_id)

        # Handle PettyCash form
        petty_cash_id = request.POST.get('petty_cash_id')
        if petty_cash_id: 
            petty_cash_instance = get_object_or_404(PettyCash, pk=petty_cash_id)
            petty_form = PettyCashForm(request.POST, instance=petty_cash_instance)
            if petty_form.is_valid():
                petty_form.save()
                return redirect('resident_detail', resident_id=resident_id)
        else:  
            petty_form = PettyCashForm(request.POST)
            if petty_form.is_valid():
                petty_cash = petty_form.save(commit=False)
                petty_cash.resident = resident
                petty_cash.save()
                return redirect('resident_detail', resident_id=resident_id)
    else:
        form = RentalFeeForm()
        petty_form = PettyCashForm()

    return render(request, 'resident_detail.html', {'form': form, 'petty_form': petty_form, 'resident': resident, 'petty_cash_types': petty_cash_types})

def delete_rental_fee(request):
    if request.method == 'POST':
        fee_id = request.POST.get('rental_fee_id')
        if fee_id:
            fee = get_object_or_404(RentalFee, pk=fee_id)
            fee.delete()
            messages.success(request, 'Rental fee deleted successfully.')
            # Pass messages to the template context
            messages_to_render = messages.get_messages(request)
            return render(request, 'resident_detail.html', {'messages': messages_to_render})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def delete_petty_cash(request):
    if request.method == 'POST':
        petty_cash = request.POST.get('petty_cash_id')
        if petty_cash:
            petty = get_object_or_404(RentalFee, pk=petty_cash)
            petty.delete()
            return JsonResponse({'message': 'Petty cash deleted successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def create_or_edit_rental_fee(request, resident_id):
    resident = get_object_or_404(Residents, pk=resident_id)
    if request.method == 'POST':
        form = RentalFeeForm(request.POST)
        if form.is_valid():
            rental_fee = form.save(commit=False)
            rental_fee.resident = resident
            rental_fee.save()
            return redirect('resident_detail', resident_id=resident_id)
    else:
        form = RentalFeeForm()
    return render(request, 'create_or_edit_rental_fee.html', {'form': form, 'resident': resident})

def create_or_edit_petty_cash(request, resident_id):
    resident = get_object_or_404(Residents, pk=resident_id)
    if request.method == 'POST':
        form = PettyCashForm(request.POST)
        if form.is_valid():
            petty_cash = form.save(commit=False)
            petty_cash.resident = resident
            petty_cash.save()
            return redirect('resident_detail', resident_id=resident_id)
    else:
        form = PettyCashForm()
    return render(request, 'create_or_edit_petty_cash.html', {'form': form, 'resident': resident})

def add_resident(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('residents_list')  
    else:
        form = ResidentForm()
    return render(request, 'add_resident.html', {'form': form})

def edit_resident(request, resident_id):
    resident = get_object_or_404(Residents, resident_id=resident_id)
    if request.method == 'POST':
        form = ResidentForm(request.POST, instance=resident)
        if form.is_valid():
            form.save()
            return redirect('residents_list')
    else:
        form = ResidentForm(instance=resident)
    return render(request, 'edit_resident.html', {'form': form})


def generate_monthly_report(request, resident_id):
    # Fetch resident object based on the resident_id
    resident = Residents.objects.get(pk=resident_id)

    # Calculate the current month and year
    today = date.today()
    current_month = today.month
    current_year = today.year

    # Calculate the month and year for last year
    last_year_month = current_month
    last_year = current_year - 1

    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="monthly_report_{resident.resident_first_name}_{resident.resident_last_name}_{current_month}_{current_year}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_heading = styles["Heading1"]
    style_normal = styles["Normal"]

    # Create report content
    content = []

    # Title
    content.append(Paragraph("Monthly Report", style_title))
    content.append(Paragraph(f"Resident: {resident.resident_first_name} {resident.resident_last_name}", style_heading))
    content.append(Paragraph(f"Date Range: {current_month}/{current_year} - {last_year_month}/{last_year}", style_heading))
    content.append(Paragraph("", style_normal))  # Add some space

    # Resident Details
    content.append(Paragraph("Resident Details:", style_heading))
    resident_table_data = [
        ["ID", "First Name", "Last Name", "Contact Name", "Relation 1", "Contact Name 2", "Relation 2"],
        [resident.resident_id, resident.resident_first_name, resident.resident_last_name, resident.contact_name,
         resident.relation1, resident.contact_name2, resident.relation2]
    ]
    resident_table = Table(resident_table_data, colWidths=[0.5 * inch] * 7)
    resident_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    content.append(resident_table)
    content.append(Paragraph("", style_normal))  # Add some space

    # Add other resident details similarly
    # You can use Paragraphs, Tables, or any other reportlab elements to structure the report

    # Build PDF
    doc.build(content)
    return response