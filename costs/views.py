from calendar import month
from unicodedata import category
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from costs.serializer import CreateUserSerializer
from .models import Category, Payment
from django.http import JsonResponse
from django.db.models import Q
import json
from rest_framework.response import Response
from datetime import date, datetime, timedelta


class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.create(user=serializer.instance)
        token_data = {"token": token.key}
        return Response(
            {**serializer.data, **token_data},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class LogoutUserAPIView(APIView):
    queryset = get_user_model().objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class Categories(APIView):
    def get(self, request, format=None):
        root = Category.objects.get(parent=None)
        children = root.build_children()
        print(children)
        return JsonResponse(children, safe=False)


class Payments(APIView):
    def get(self, request, format=None):
        datetoday = date.today()
        monthago = datetoday-timedelta(days=30)
        payments = Payment.objects.filter(user_id=self.request.user).filter(
            date__lte=request.GET.get('to', datetoday)).filter(date__gte=request.GET.get('from', monthago))
        if request.GET.get('category'):
            payments = payments.filter(category=request.GET.get('category'))
        paymentdata = []
        for payment in payments:
            paymentdata.append({
                'id': payment.id,
                'name': payment.name,
                'price': payment.price,
                'category': payment.category,
                'date': payment.date,
            })
        return JsonResponse(paymentdata, safe=False)

    def post(self, request, format=None):
        request = request.body.decode('utf-8')
        request = json.loads(request)
        name = request['name']
        price = request['price']
        category = request['category']
        payment = Payment(name=name, price=price, category=category)
        payment.save()
        return JsonResponse({'Good Request': 'Ok'})
