from calendar import month
from unicodedata import category
from xxlimited import Null
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from costs.serializer import CreateUserSerializer
from .models import Category, Payment, Venders
from django.http import JsonResponse
from django.db.models import Q
import json
from rest_framework.response import Response
from datetime import date, datetime, timedelta
from django.db.models import Sum
import calendar
import io
import csv
import pandas as pd
from decimal import Decimal
import datetime
import unidecode


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
        return JsonResponse(children, safe=False)


class Payments(APIView):
    def get(self, request, format=None):
        datetoday = date.today()
        monthago = datetoday-timedelta(days=30)
        payments = Payment.objects.filter(user=self.request.user).filter(
            date__lte=request.GET.get('to', datetoday)).filter(date__gte=request.GET.get('from', monthago))
        if request.GET.get('category'):
            category = Category.objects.get(id=request.GET.get('category'))
            betapayment = category.get_payments(payments)

            payments = betapayment
        paymentdata = []
        for payment in payments:
            paymentdata.append({
                'id': payment.id,
                'name': payment.name,
                'price': payment.price,
                'category': payment.category.name,
                'date': payment.date,
            })
        response = {}
        response["data"] = paymentdata

        sum = 0
        for payment in paymentdata:
            sum = sum + payment["price"]
        response["sum"] = sum

        return JsonResponse(response, safe=False)

    def post(self, request, format=None):
        request = request.body.decode('utf-8')
        request = json.loads(request)
        name = request['name']
        price = request['price']
        date = request['date']
        user = self.request.user
        try:
            category = Category.objects.get(id=request['category'])
        except:
            return JsonResponse({'Bad Request': 'Category not found'})
        payment = Payment(name=name, price=price,
                          category=category, user=user, date=date)
        payment.save()
        return JsonResponse({'Good Request': 'Ok'})

    def put(self, request, format=None):
        request = request.body.decode('utf-8')
        request = json.loads(request)
        payment = Payment.objects.filter(user=self.request.user).filter(
            id=request['id'])[0]
        if payment.name != request['name']:
            payment.name = request['name']
        if payment.price != request['price']:
            payment.price = request['price']
        if payment.date != request['date']:
            payment.date = request['date']
        category = Category.objects.get(id=request['category'])
        payment.category = category
        payment.save()
        if request['rememberVender'] == True:
            vender = Venders(name=request['name'], category=category)
            vender.save()
        return JsonResponse({'Good Request': 'Ok'})


class Paymentid(APIView):
    def delete(self, request, id, format=None):
        Payment.objects.get(id=id).delete()
        return JsonResponse({'Good Request': 'Ok'})


class Statistic(APIView):
    def get(self, request, id, format=None):
        category = Category.objects.get(id=id)
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))
        day = calendar.monthrange(year, month)
        first = date(year, month, 1)
        last = date(year, month, day[1])
        number = Payment.objects.filter(user=self.request.user).filter(
            date__lte=last).filter(date__gte=first).count()
        if number == 0:
            response = {"General": [{"name": "no data",
                                    "sum": 0, "proportion": 0, "id": 0}]}
            return JsonResponse(response, safe=False)
        payments = Payment.objects.filter(user=self.request.user).filter(
            date__lte=last).filter(date__gte=first)
        response = category.get_statistic(payments)
        print(response)
        return JsonResponse(response, safe=False)


class Fileuploader(APIView):
    def post(self, request, format=None):
        myfile = request.FILES["myFile"]

        df = pd.read_csv(myfile,
                         sep=",",
                         header=0,
                         usecols=["Name", "Sum", "Date"])
        df1 = pd.DataFrame(df, columns=["Name", "Sum", "Date"])
        for row in range(0, len(df1)):
            id = Category.objects.get(id=31)
            vname = df1.iloc[row]["Name"]
            try:
                vprice = -Decimal(df1.iloc[row]["Sum"])
            except:
                vprice = unidecode.unidecode(df1.iloc[row]["Sum"])
                vprice = - \
                    Decimal(float(vprice.replace(" ", "").replace(",", ".")))
            if vprice < 0:
                continue
            vdate = df1.iloc[row]["Date"]
            try:
                vdate = datetime.datetime.strptime(
                    vdate, "%m/%d/%Y").strftime("%Y-%m-%d")
            except:
                vdate = datetime.datetime.strptime(
                    vdate, "%d.%m.%Y").strftime("%Y-%m-%d")
            if Venders.objects.filter(specific__contains=[vname]):
                ven = Venders.objects.filter(specific__contains=[vname])
                id = ven[0].category
            else:
                vendors = Venders.objects.all()
                for vendor in vendors:
                    if vendor.name in vname:
                        vendor.specific.append(vname)
                        vendor.save()
                        id = vendor.category

            payment = Payment(name=vname, price=vprice,
                              category=id, user=self.request.user, date=vdate)
            payment.save()
        return JsonResponse({'Good Request': 'Ok'})
