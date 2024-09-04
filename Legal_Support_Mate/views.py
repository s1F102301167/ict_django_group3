from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'Legal_Support_Mate/index.html')

def talk(request, category: str):
    print(category)
    messages = []
    ans = []
    if request.method == 'POST':
        msg = request.POST['message']
        messages.append(msg)
        ans.append(gpt_response(msg))
    context = {
        'category': category,
        'messages': messages,
        "gpt_anser": ans
    }
    return render(request, 'Legal_Support_Mate/talk.html', context)

def gpt_response(question: str) -> str:
    a = call_gpt(question)
    return a

def call_gpt(_: str) -> str:
    return "gpt answer"
