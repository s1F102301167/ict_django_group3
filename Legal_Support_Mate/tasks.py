import os
## Chat Modelsを使うときはChatOpenAIをインポート
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain import PromptTemplate
## Chainを読み込む
from langchain import LLMChain

def call_gpt(question: str, category: str) -> str:
    #APIキーの登録
    os.environ["OPENAI_API_KEY"] = "hp_v8CJhGZOsPl_QHsF1oW6w9lzvA-B5QGi3sQS_DNKBmDe_TUvLlAg95Y_rDzk4ikTu5_yqB5ja8zrYqq5A_iw"

    url = "https://api.openai.iniad.org/api/v1/"
    # OpenAI埋め込みモデルのインスタンスを作成
    embeddings_model = OpenAIEmbeddings(
        openai_api_base= url
    )

    # 複数のPDFファイルパスをリストで指定
    pdf_paths = [f for f in [
        "Legal_Support_Mate/pdf/パワハラ1.pdf",
        "Legal_Support_Mate/pdf/パワハラ2.pdf",
        "Legal_Support_Mate/pdf/パワハラ3.pdf",
        "Legal_Support_Mate/pdf/パワハラ4.pdf",
        "Legal_Support_Mate/pdf/消費者法1.pdf",
        "Legal_Support_Mate/pdf/消費者法2.pdf",
        "Legal_Support_Mate/pdf/相続権1.pdf",
        "Legal_Support_Mate/pdf/相続権2.pdf",
        "Legal_Support_Mate/pdf/相続権3.pdf",
        "Legal_Support_Mate/pdf/道路交通1.pdf",
        "Legal_Support_Mate/pdf/道路交通2.pdf",
        "Legal_Support_Mate/pdf/道路交通3.pdf",
        "Legal_Support_Mate/pdf/道路交通4.pdf",
        "Legal_Support_Mate/pdf/道路交通5.pdf",
        "Legal_Support_Mate/pdf/著作権.pdf",
        "Legal_Support_Mate/pdf/誹謗中傷1.pdf",
        "Legal_Support_Mate/pdf/誹謗中傷2.pdf",
        "Legal_Support_Mate/pdf/誹謗中傷3.pdf",
        "Legal_Support_Mate/pdf/離婚1.pdf",
        "Legal_Support_Mate/pdf/離婚2.pdf",
        "Legal_Support_Mate/pdf/労働1.pdf",] if category in f
    ]

    all_text = ""
    for pdf_path in pdf_paths:
        loader = PyPDFLoader(pdf_path)
        pdf_text = "\n".join([page.page_content for page in loader.load()])
        all_text += pdf_text + "\n"


    # Text Splitterの設定
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )

    # テキストの分割
    documents = text_splitter.create_documents([all_text])

    # ベクトル化したテキストをChromaDBに保存する
    db = Chroma.from_documents(documents,embeddings_model)

    # ドキュメントの読み込みとベクトルストアの作成
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # テンプレートとプロンプトの定義
    template_with_context = """アナタは最高の弁護士です。
    #制約内容に沿って最適な対処法を限りなく法律に沿って順詳しく悩みを解決してあげてください。
    #制約内容
    1.読み込んだデータに基づき法律に沿いアドバイスをしてください。
    2.親身になって相談を聞いてあげてください。
    3.相手の文章から反省の色が見えなか#例に沿って判断し不適切な場合は強く警告してあげてください。
    そのあとに法律のみに沿い対処法を順に沿って詳しく教えてあげてください。
    例)やったぜ、殺したぜ、轢いてやったぜ、最高、爽快等
    {context}
    質問: {question}
    """

    prompt_with_context = ChatPromptTemplate.from_template(template_with_context)

    # LLMの定義（ストリーミング対応）
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
        openai_api_base= url,
        verbose=True)

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    # Chainの定義
    chain_with_context = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt_with_context
        | llm
        | StrOutputParser()
    )

    def process_query_with_rag(query):
        # 関連ドキュメントの取得
        relevant_docs = retriever.get_relevant_documents(query)
        sources = [doc.page_content for doc in relevant_docs]

        # 回答の生成（ストリーミング）
        answer = ""
        for chunk in chain_with_context.stream(query):
            answer += chunk
            print(answer)
            yield answer, "\n\n".join(sources)

    return "".join([p[0] for p in process_query_with_rag(question)][-1])


##時間のAPIを利用
import requests

# テキストデータを指定された URL から取得する関数
def fetch_time_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP エラーが発生した場合に例外をスロー
        return response.text  # 生のテキストデータを返す
    except requests.RequestException as e:
        print(f"エラーが発生しました: {e}")
        return None

# 時刻データの URL
time_data_url = "http://www.openspc2.org/data/date/full.txt"

# 時刻データを取得して表示する
def return_time():
    time_data = fetch_time_data(time_data_url)
    if time_data:
        T = []
        for i, time in enumerate(time_data.split("\n")):
            if i == 3 :continue
            T.append(time)

    return  "/".join(T[0:3])+" "+":".join(T[3:5])
  # 2024/9/5 14:5
