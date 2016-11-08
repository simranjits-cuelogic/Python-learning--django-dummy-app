# for render views
from django.shortcuts import render, get_object_or_404

# for HttpResponse
from django.http import HttpResponse
from django.template import loader

# import Http404
# from django.http import Http404

# import Question model
from .models import Question

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
    response = "You're looking at the results of question %s"
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("you're voting on question %s." % question_id)

