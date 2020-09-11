from django.db import models


# Create your models here.


class Tag(models.Model):
    content = models.CharField(max_length=32)
    color = models.CharField(max_length=8)


class Task(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,)
    status = models.IntegerField()
    introduce = models.TextField()
    startTime = models.DateTimeField()
    deadLine = models.DateTimeField()
    acceptTime = models.DateTimeField(blank=True, null=True)
    startDep = models.IntegerField()
    receiveDep = models.IntegerField()
    fileAddress = models.CharField(max_length=100)
    fileName = models.CharField(max_length=100)


class Done(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,)
    doneTime = models.DateTimeField()
    doneFileAddress = models.CharField(max_length=100)
    doneFileName = models.CharField(max_length=100)
    zanList = models.CharField(max_length=12, default="100")
    message = models.TextField()


class User(models.Model):
    status = models.IntegerField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    qqEmail = models.EmailField()
    phone = models.IntegerField()
