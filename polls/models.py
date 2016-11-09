from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone

# import Http404
from django.http import Http404

# query set chaining for custion filters (ie. Class level fiters)
class QuestionQuerySet(models.query.QuerySet):
    def recent(self):
        return self.filter(pub_date__lte = timezone.now()
        ).order_by('-pub_date')[:5]

    # dummy method for testing method chaining
    def recent1(self):
        return self.filter(pub_date__gte = timezone.now() - datetime.timedelta(
            days=7)
        )

    def get_question(self, id):
        """return question or raise exception  -- custom method"""
        try:
            return Question.objects.get(id = id)
        except Question.DoesNotExist:
            raise Http404('Question does not exist.')

class QuestionManager(models.Manager):
    def get_query_set(self):
        return QuestionQuerySet(self.model, using=self._db)

    def recent(self):
        return self.get_query_set().recent()

    def recent1(self):
        return self.get_query_set().recent1()

    def get_question(self, id):
        """return question or raise exception -- custom method"""
        return self.get_query_set().get_question(id)


# Note: Question has-many choices -- Relation is one-to-many
class Question(models.Model):
    """
    Question model that contain all the question related to the system.
    """
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    objects = QuestionManager()

    def __str__(self):
        return self.question

    # instance method
    def latest_posted(self):
        """Boolean <= is post latest or not"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    latest_posted.admin_order_field = 'pub_date'
    latest_posted.boolean = True
    latest_posted.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
