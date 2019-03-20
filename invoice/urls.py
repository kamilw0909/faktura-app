from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'invoice'
urlpatterns = [
    # np. /
    path('', login_required(views.IndexView.as_view()), name='index'),
    # np. /1/
    path('<int:invoice_id>/', views.detail, name='detail'),
    path('edit/<int:invoice_id>', views.edit, name='edit'),
    path('new/', views.new_invoice, name='new_invoice'),
    path('download/<int:invoice_id>', views.download, name='download'),
]
