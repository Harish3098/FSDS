from django.db import models

# Create your models here.
class admin_user(models.Model):

    UserName = models.CharField(max_length=25 )
    Password = models.CharField(max_length=25 )
    def __str__(self):
        return self.UserName


class Feedback(models.Model):

    stu_UserName = models.CharField(max_length=25 )
    feedback_info = models.CharField(max_length=100 )
    def __str__(self):
        return self.stu_UserName