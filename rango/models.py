from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)

	def __unicode__(self):
		return self.name
	class Meta:
		verbose_name_plural = "Categories"

class Page(models.Model):
	title = models.CharField(max_length=128)
	category = models.ForeignKey(Category)
	url = models.URLField()
	views = models.IntegerField(default=0)

	def __unicode__(self):
		return self.title