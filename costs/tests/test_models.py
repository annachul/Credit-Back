from django.test import TestCase
from ..models import Category, Payment
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.test import Client
from datetime import date, timedelta, datetime


class CategoryMdelTests(TestCase):
    def test_build_children(self):
        category1 = Category(id=1, name="sport")
        category1.save()
        category2 = Category(id=2, name="football", parent=category1)
        category2.save()
        category3 = Category(id=3, name="skiing", parent=category1)
        category3.save()
        category4 = Category(id=4, name="soocer", parent=category2)
        category4.save()
        category5 = Category(id=5, name="american football", parent=category2)
        category5.save()

        result = {"name": "sport", "id": 1, "children": [{"name": "football", "id": 2, "children": [{"name": "soocer", "id": 4, "children": [{"name": "all soocer", "id": 4}]}, {"name": "american football", "id": 5, "children": [
            {"name": "all american football", "id": 5}]}, {"name": "all football", "id": 2}]}, {"name": "skiing", "id": 3, "children": [{"name": "all skiing", "id": 3}]}, {"name": "all sport", "id": 1}]}

        self.assertEqual(category1.build_children(), result)

    def test_get_payments(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        category1 = Category(id=1, name="sport")
        category1.save()
        category2 = Category(id=2, name="football", parent=category1)
        category2.save()
        category3 = Category(id=3, name="skiing", parent=category1)
        category3.save()
        category4 = Category(id=4, name="soocer", parent=category2)
        category4.save()
        category5 = Category(id=5, name="american football", parent=category2)
        category5.save()
        payment1 = Payment(id=1, name="field", price=90.98,
                           category=category2, date=date.today(), user=user)
        payment1.save()
        payment2 = Payment(id=2, name="ski", price=67.91,
                           category=category3, date=date.today(), user=user)
        payment2.save()
        payment3 = Payment(id=3, name="ball", price=10.89,
                           category=category4, date=date.today(), user=user)
        payment3.save()
        payment4 = Payment(id=4, name="form", price=35.35,
                           category=category5, date=date.today(), user=user)
        payment4.save()
        payments = Payment.objects.all()
        category = category2
        betapayment = category.get_payments(payments)
        lencon = len(betapayment)
        self.assertEqual(lencon, 3)

    def test_get_statistic(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        category1 = Category(id=1, name="sport")
        category1.save()
        category2 = Category(id=2, name="football", parent=category1)
        category2.save()
        category3 = Category(id=3, name="skiing", parent=category1)
        category3.save()
        category4 = Category(id=4, name="soocer", parent=category2)
        category4.save()
        category5 = Category(id=5, name="american football", parent=category2)
        category5.save()
        payment1 = Payment(id=1, name="field", price=90.98,
                           category=category2, date=date.today(), user=user)
        payment1.save()
        payment2 = Payment(id=2, name="ski", price=67.91,
                           category=category3, date=date.today(), user=user)
        payment2.save()
        payment3 = Payment(id=3, name="ball", price=10.89,
                           category=category4, date=date.today(), user=user)
        payment3.save()
        payment4 = Payment(id=4, name="form", price=35.35,
                           category=category5, date=date.today(), user=user)
        payment4.save()
        payments = Payment.objects.all()
        result = category1.get_statistic(payments)

        sum = 0
        for cat in result[category1.name]:
            sum = sum+cat["sum"]
        self.assertEqual(float(sum), 205.13)
        prop = 0
        for cat in result[category1.name]:
            prop = prop+cat["proportion"]
        self.assertEqual(float(prop), 1)
        len1 = len(result[category1.name])
        self.assertEqual(float(len1), 2)
        football_result = category2.get_statistic(payments)
        sum = 0
        for cat in football_result[category2.name]:
            sum = sum+cat["sum"]
        self.assertEqual(float(sum), 137.22)
        prop = 0
        for cat in football_result[category2.name]:
            prop = prop+cat["proportion"]
        self.assertEqual(float(prop), 1)
        len1 = len(football_result[category2.name])
        self.assertEqual(float(len1), 3)
