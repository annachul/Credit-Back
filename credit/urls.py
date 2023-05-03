from django.contrib import admin
from django.urls import path
from django.urls import path, include
from costs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("costs.urls")),
    path('api/categories', views.Categories.as_view(), name="categories"),
    path('api/payments', views.Payments.as_view(), name="payments"),
    path('api/categories/<id>', views.Statistic.as_view(), name="statistic"),
    path('api/payments/fileuploader',
         views.Fileuploader.as_view(), name="fileuploader"),
    path('api/payments/<id>', views.Paymentid.as_view(), name="paymentid"),
]
