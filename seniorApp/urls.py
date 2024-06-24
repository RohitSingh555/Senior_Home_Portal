from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # path('login/', views.my_login_view, name='login'),
    # path('logout/', views.my_logout_view, name='logout'),
    path('', login_required(views.residents_list), name='residents_list'),
    path('search/', login_required(views.search_residents), name='search_residents'),
    path('resident/<int:id>/', login_required(views.resident_detail), name='resident_detail'),
    path('add_resident/', login_required(views.add_resident), name='add_resident'),
    path('email_logs/', login_required(views.email_logs), name='email_logs'),
    path('edit_resident/<int:id>/', login_required(views.edit_resident), name='edit_resident'),
    # path('delete_rental_fee/', login_required(views.delete_rental_fee, name='delete_rental_fee'),
    # path('delete_petty_cash/', login_required(views.delete_petty_cash, name='delete_petty_cash'),
    #  path('reports/monthly/<int:resident_id>', login_required(views.generate_monthly_report, name='monthly_report'),
    path('reports/view/<int:id>', login_required(views.generate_report), name='view_report'),
    path('reports/viewreport', login_required(views.view_my_report), name='view_my_report'),
    path('generate_pdf/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.generate_pdf), name='generate_pdf'),
    path('generate_pdf_petty/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.generate_pdf_petty), name='generate_pdf_petty'),
    path('generate_yearly_pdf/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.generate_yearly_pdf), name='generate_yearly_pdf'),
    path('send_email_yearly/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.sendemail_yearly), name='sendemail_yearly'),
    path('send_email_petty/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.sendemail_pdf_petty), name='sendemail_pdf_petty'),
    path('send_email_rental/<int:id>/<str:startdate>/<str:enddate>/', login_required(views.sendemail_pdf_rental), name='sendemail_pdf_rental'),

    # path('reports/yearly/<int:resident_id>', login_required(views.generate_monthly_report, name='yearly_report'),
]
