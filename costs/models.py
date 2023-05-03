from unicodedata import category
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.id}'

    def build_children(self):
        result = {"name": self.name, "id": self.id}
        children = self.children.all()
        if children == None:
            return result
        else:
            arr_children = []
            for child in children:
                arr_children.append(child.build_children())
            name = "all " + self.name
            arr_children.append({"name": name, "id": self.id})
            result["children"] = arr_children
            return result

    def get_payments(self, payments):
        children = self.children.all()
        betapayment = []
        if not children:
            payments_array = payments.filter(category=self)
            for paynemt in payments_array:
                betapayment.append(paynemt)
            return betapayment
        else:
            for child in children:
                result = child.get_payments(payments)
                betapayment.extend(result)
            payment_self = payments.filter(category=self)
            for paynemt in payment_self:
                betapayment.append(paynemt)
            return betapayment

    def get_statistic(self, payments):
        children = self.children.all()
        list_children = []
        all_payments = self.get_payments(payments)
        sum = 0
        all_child_sum = 0
        for payment in all_payments:
            sum = sum + payment.price
        for child in children:
            child_payments = child.get_payments(payments)
            child_sum = 0

            for payment in child_payments:
                child_sum = child_sum + payment.price
            all_child_sum = all_child_sum+child_sum
            proportion = child_sum/sum
            child_result = {"name": child.name,
                            "sum": float(child_sum), "proportion": round(proportion, 2), "id": child.id}
            list_children.append(child_result)
        if all_child_sum != sum:

            all_sum = sum-all_child_sum
            proportion_all = all_sum/sum
            name = "all " + self.name
            all_result = {"name": name,
                          "sum": float(all_sum), "proportion": round(proportion_all, 2), "id": self.id}
            list_children.append(all_result)
        result = {self.name: list_children}
        return result


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=700)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    date = models.DateField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.id}'


class Venders(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    specific = ArrayField(models.CharField(
        max_length=255), null=False, default=list)

    def __str__(self):
        return f'{self.name} - {self.id}'
