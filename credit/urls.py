from django.contrib import admin
from django.urls import path
from django.urls import path, include
from costs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("costs.urls")),
    path('api/categories', views.Categories.as_view(), name="categories"),
    path('api/payments', views.Payments.as_view(), name="payments")
]
