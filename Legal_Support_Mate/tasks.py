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
    pdf_paths = [
        # "/交通安全対策基本法.pdf",
        # "/道路交通法.pdf"
        "C:\\Users\\iniad\\Downloads\\security-reference-architecture.pdf"
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
    template_with_context = """以下のcontextのみに基づいて質問にできるだけ詳しく箇条書きで答えなさい。:
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
