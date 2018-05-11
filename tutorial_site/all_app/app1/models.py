from django.db import models
from django.utils import timezone
# Create your models here.
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField()
	def __str__(self):
		return self.question_text
	def some_function(self):
		return ('something')
class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	number = models.IntegerField(default=0)
	def __str__(self):
		return self.choice_text
# ForeignKey means multiple Choice are mapped to one Question
# some operation
# Question.objects.all()
# Question.objects.filter(question_text__startwith='something'), where '__' represent some sort of '.'
# Question.objects.get(id=1)
# q = Question(question_text="some text", pub_date=timezone.now())
# q.choice_set, means all Choices that are mapped to Question, support count(), all(), etc.
# q.save(), save to db
# q.delete()
# q.choice_set.create(choice_text='something', number=10)