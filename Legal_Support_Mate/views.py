from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from .models import Message
from .tasks import call_gpt, return_time, stream_test
import markdown
import re
def index(request):
    return render(request, 'Legal_Support_Mate/index.html')
def sse_view(request, category: str):
    user_message = request.GET.get('user_message', "NULL")
    # FIXME: 前回と同じ質問を送信した場合、bot_responseが更新されない
    def event_stream():
        md = markdown.Markdown()
        # Fetch the result from call_gpt generator function
        for response in call_gpt(user_message, category):
            response = re.sub(r'\n+', '<br>', response)
            md_response = md.convert(response)
            # Update the bot response in the database (optional)

            # Send response via SSE
            yield f"data: {md_response}\n\n"
        Message.objects.update_or_create(user_message=user_message,
                                            category=category,
                                            defaults={'bot_response': md_response})
        yield f"data: done\n\n"
    # Set content_type to 'text/event-stream' for SSE
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')

def talk(request, category: str):
    # FIXME: talkは実際には呼ばれないのでメッセージの保存がされない
    # メッセージが揮発性になるだけで、致命的な問題はない
    if request.method == 'POST':
        user_message = request.POST.get('user_message')
#        redirect('sse', category=category)
        # Redirect to SSE view after form submission
        return render(request, 'Legal_Support_Mate/talk.html', {
            'category': category,
            "messages": Message.objects
                .filter(category=category)
                .order_by('-created_at'),
            "time": return_time()
        })

    # Fetch previous messages
    messages = Message.objects.filter(category=category).order_by('created_at')

    return render(request, 'Legal_Support_Mate/talk.html', {
        'category': category,
        'messages': messages,
        'time': return_time()
    })

def clear(request, category: str):
    Message.objects.filter(category=category).delete()
    return redirect('talk', category=category)
