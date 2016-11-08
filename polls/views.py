# for render views
from django.shortcuts import render, get_object_or_404

# for HttpResponse
from django.http import HttpResponse
from django.template import loader

# import Http404
# from django.http import Http404

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# import Question model
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_questions' : latest_question_list
    }
    # dept. on HttpResponse, loader
    # template = loader.get_template('polls/index.html')
    # return HttpResponse(template.render(context, request))

    # dept. on render
    return render(request, 'polls/index.html', context)

def profile(request):
    return HttpResponse("Hello, world. Profile here.")

def detail(request, question_id):
    # custom method in Question model
    # question = Question.objects.get_question(question_id)

    # dept. on get_object_or_404
    question = get_object_or_404(Question, pk=question_id)

    context = {'question' : question}
    # dept. on render
    return render(request, 'polls/details.html', context)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

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
