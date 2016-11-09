# for render views
from django.shortcuts import render, get_object_or_404

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

# import Question model
from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.recent()

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the question voting form
        return render(request, 'polls/details.html' , {
            'question' : question,
            'error_message' : "You didn\'t select a choice."
            })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # Always return and HttpResponseRedirect after succesfully dealing
        # with POST data. This porevents data from being posted twice if a
        # user hits the back button.
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,) ))
