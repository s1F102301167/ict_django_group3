from django.db import models

# Create your models here.
class Message(models.Model):
    category = models.CharField(max_length=255)  # 質問のカテゴリ
    user_message = models.TextField()  # ユーザーが入力した質問
    bot_response = models.TextField(null=True, blank=True)  # Web APIからの回答（初めはnull）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時
