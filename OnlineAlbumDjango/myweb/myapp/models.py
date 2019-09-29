from django.db import models
from datetime import datetime
# Create your models here.


class Photos(models.Model):
	title = models.CharField(max_length=32)
	photo_name = models.CharField(max_length=32)
	addtime = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return "%d,%s：%s"%(self.id,self.title,self.photo_name)

