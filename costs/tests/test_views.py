from django.test import Client
from django.test import TestCase
from ..models import Category, Payment
from django.urls import reverse
from datetime import date, timedelta, datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class PaymentsViewTests(TestCase):

    def test_get_payments(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        client = Client()
        self.client.login(username='testuser', password='12345')
        token = Token.objects.create(user=user)
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
        response = self.client.get(
            reverse('payments'), HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        sum = json_response["sum"]
        self.assertEqual(sum, '205.13')

    def test_post_payments(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        client = Client()
        self.client.login(username='testuser', password='12345')
        token = Token.objects.create(user=user)
        category1 = Category(id=1, name="sport")
        category1.save()
        data = {"name": "form", "price": "95.45", "category": "1"}
        response = self.client.post(reverse(
            'payments'), data, content_type='application/json', HTTP_AUTHORIZATION='Token {}'.format(token))
        self.assertEqual(response.status_code, 200)


class StatisticsViewTests(TestCase):
    def test_get_sttistic(self):
        user = User.objects.create_user(username='testuser', password='12345')
        user.save()
        client = Client()
        self.client.login(username='testuser', password='12345')
        token = Token.objects.create(user=user)
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
        currentMonth = datetime.now().month
        currentYear = datetime.now().year
        response = self.client.get(
            "/api/categories/1", {'month': currentMonth, 'year': currentYear}, HTTP_AUTHORIZATION='Token {}'.format(token))
        json_response = response.json()
        self.assertEqual(response.status_code, 200)
        sum = 0
        for cat in json_response[category1.name]:
            sum = sum+float(cat['sum'])
        self.assertEqual(sum, 205.13)
