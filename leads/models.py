from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime
import random
# Create your models here.



class Lead(models.Model):
    lead_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30, unique=False, blank=False)
    last_name = models.CharField(max_length=30, unique=False, blank=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    email = models.CharField(max_length=50, unique=False)
    credit = models.CharField(max_length=3, blank=False)
    date_created = models.DateField(auto_now_add=True)
    last_contacted = models.DateField(null=True)
    last_contact_method = models.CharField(max_length=30, unique=False, null=True)
    log = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    @property
    def days_since_contact(self):
        todays = str(date.today())
        today = datetime.strptime(todays, "%Y-%m-%d")
        date_str = str(self.last_contacted)
        d = datetime.strptime(date_str, "%Y-%m-%d")
        return abs((today - d).days)


    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name

class QualTable(models.Model):
    lead_id = models.OneToOneField(Lead, on_delete=models.CASCADE)
    table_id = models.AutoField(primary_key=True)
    loan_type = models.TextField(blank=True, null=True, default = 'FHA')
    price = models.IntegerField(blank=True, null=True, default = 200000)
    down_payment = models.FloatField(blank=True, null=True, default = 3.5)
    rate = models.FloatField(blank=True, null=True, default = 4.00)
    HOA_dues = models.FloatField(blank=True, null=True, default = 0)
    monthly_payment = models.FloatField(blank=True, null=True)
    term = models.IntegerField(blank=True, null=True, default = 360)

@receiver(post_save, sender=Lead)
def create_qual_table(sender, instance, created, **kwargs):
    if created:
        QualTable.objects.create(lead_id=instance)
