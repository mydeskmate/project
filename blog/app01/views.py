from django.shortcuts import render,HttpResponse,redirect
from . import models
# Create your views here.

def index(request):
    type_choice_list = models.Article.type_choices
    return render(request,'index.html',
    {
        'type_choice_list':type_choice_list,
    })
