from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message
from .tasks import call_gpt

def index(request):
    return render(request, 'Legal_Support_Mate/index.html')

def talk(request, category: str):
    if request.method == 'POST':
        msg = request.POST['user_message']
        bot_response = call_gpt(msg, category)
        Message.objects.create(category=category, user_message=msg, bot_response=bot_response)
        return redirect('talk', category)
    context = {
        'category': category,
        'messages': Message.objects
                .filter(category=category)
                .order_by('created_at')
    }
    return render(request, 'Legal_Support_Mate/talk.html', context)

def clear(request, category: str):
    Message.objects.filter(category=category).delete()
    return redirect('talk', category=category)
