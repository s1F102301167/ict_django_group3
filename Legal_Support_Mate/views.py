from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Message
from .tasks import call_gpt, return_time
import markdown

def index(request):
    return render(request, 'Legal_Support_Mate/index.html')

def talk(request, category: str):
    if request.method == 'POST':
        md = markdown.Markdown()
        msg = request.POST['user_message']
        bot_response = md.convert(call_gpt(msg, category))
        Message.objects.create(category=category, user_message=msg, bot_response=bot_response)
        return redirect('talk', category)
    time = return_time()
    print(time)
    context = {
        'category': category,
        'messages': Message.objects
                .filter(category=category)
                .order_by('created_at'),
        'time': time
    }
    return render(request, 'Legal_Support_Mate/talk.html', context)

def clear(request, category: str):
    Message.objects.filter(category=category).delete()
    return redirect('talk', category=category)
