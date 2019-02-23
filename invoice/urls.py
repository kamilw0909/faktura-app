from django.urls import path

from . import views

app_name='invoice'
urlpatterns = [
    # np. /
    path('', views.index, name='index'),
    # np. /1/
    path('<int:invoice_id>/', views.detail, name='detail'),
]
