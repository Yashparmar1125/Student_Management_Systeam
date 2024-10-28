from django.db import models
from users.models import Student

class Person(models.Model):
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    prs_nbr = models.AutoField(primary_key=True)
    prs_name = models.CharField(max_length=100)
    prs_skill = models.CharField(max_length=100)

class Attendance(models.Model):
    accs_id = models.AutoField(primary_key=True)
    accs_prsn = models.ForeignKey(Person, on_delete=models.CASCADE)
    accs_date = models.DateField(auto_now_add=True)
    accs_added = models.DateTimeField(auto_now_add=True)

class ImageDataset(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_person = models.ForeignKey(Person, on_delete=models.CASCADE)

