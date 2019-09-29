from django.db import models

# Create your models here.

class Stu(models.Model):
    name = models.CharField(max_length=16)
    age = models.IntegerField()
    classid = models.CharField(max_length=20)

    def __str__(self):
        return '%s:%d:%s'%(self.name, self.age, self.classid)

    class Meta:
        db_table = 'stu'