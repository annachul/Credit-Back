from unicodedata import category
from django.db import models
from django.conf import settings


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
                result["children"] = arr_children
            return result


class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    price = models.FloatField(null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} - {self.id}'
