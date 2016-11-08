from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

# query set chaining for custion filters (ie. Class level fiters)
class QuestionQuerySet(models.query.QuerySet):
    def recent(self):
        return self.filter(pub_date__gte = timezone.now() - datetime.timedelta(
            days=7)
        )

    def recent1(self):
        return self.filter(pub_date__gte = timezone.now() - datetime.timedelta(
            days=7)
        )

class QuestionManager(models.Manager):
    def get_query_set(self):
        return QuestionQuerySet(self.model, using=self._db)

    def recent(self):
        return self.get_query_set().recent()

    def recent1(self):
        return self.get_query_set().recent1()


# Note: Question has-many choices -- Relation is one-to-many
class Question(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    objects = QuestionManager()

    def __str__(self):
        return self.question

    # instance method
    def latest_posted(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text