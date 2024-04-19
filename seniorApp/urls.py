from django.urls import path
from . import views

urlpatterns = [
    path('', views.residents_list, name='residents_list'),
    path('search/', views.search_residents, name='search_residents'),
    path('resident/<int:id>/', views.resident_detail, name='resident_detail'),
    path('add_resident/', views.add_resident, name='add_resident'),
    path('edit_resident/<int:id>/', views.edit_resident, name='edit_resident'),
    # path('delete_rental_fee/', views.delete_rental_fee, name='delete_rental_fee'),
    # path('delete_petty_cash/', views.delete_petty_cash, name='delete_petty_cash'),
    #  path('reports/monthly/<int:resident_id>', views.generate_monthly_report, name='monthly_report'),
    path('reports/view/<int:id>', views.generate_report, name='view_report'),
    path('reports/viewreport', views.view_my_report, name='view_my_report'),
    path('generate_pdf/<int:id>/<str:startdate>/<str:enddate>/', views.generate_pdf, name='generate_pdf'),
    path('generate_pdf_petty/<int:id>/<str:startdate>/<str:enddate>/', views.generate_pdf_petty, name='generate_pdf_petty'),
    path('generate_yearly_pdf/<int:id>/<str:startdate>/<str:enddate>/', views.generate_yearly_pdf, name='generate_yearly_pdf'),

    # path('reports/yearly/<int:resident_id>', views.generate_monthly_report, name='yearly_report'),
]
