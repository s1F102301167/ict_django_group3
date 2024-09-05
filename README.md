# legal support mateアプリ
## ダウンロード

### 手順
1. レポジトリのクローン
```bash
git clone git@github.com:s1F102301167/ict_django_group3.git
```

2. プロジェクトのディレクトリに移動
```bash
cd ict_django_group3
```

3. python仮想環境の構築
```bash
python -m venv venv
```

4. 仮想環境の起動
```bash
.\venv\Scripts\activate
```

5. djangoのインストール
```bash
pip install django langchain langchain-community openai langchain_openai pypdf tiktoken chromadb cryptography markdown
```

7. マイグレーションをする
```bash
python manage.py migrate
```

8. サーバー起動
```bash
python manage.py runserver
```

9. http://127.0.0.1:8000/Legal_Support_Mate
にアクセス
