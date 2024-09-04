from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'Legal_Support_Mate/index.html')

def talk(request, category: str):
    print(category)
    context = {
        'category': category
    }
    return render(request, 'Legal_Support_Mate/talk.html', context)

