# pip install langchain chromadb pypdf ollama tqdm langchain-chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from tqdm import tqdm

def load_pdf(pdf_path):
    """加载 PDF 文档"""
    print(" 正在加载 PDF...")
    loader = PyPDFLoader(pdf_path)
    return loader.load()

def split_text(documents):
    """将文档分割成文本块"""
    print(" 正在拆分文本...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return list(tqdm(text_splitter.split_documents(documents), desc=" 文本块处理"))

def load_or_create_chroma_db(chunks, embedding, db_path):
    """加载或创建 Chroma 向量数据库"""
    try:
        print(" 尝试加载现有向量数据库...")
        vector_db = Chroma(persist_directory=db_path, embedding_function=embedding)
        print("✅ 已加载现有向量数据库")
    except:
        print("⚡ 创建新的向量数据库...")
        vector_db = Chroma.from_documents(chunks, embedding, persist_directory=db_path)
        print("✅ 新数据库创建完成")
    return vector_db

def add_data_to_chroma_db(vector_db, chunks):
    """向 Chroma 数据库追加新数据"""
    print(" 正在追加新数据到数据库...")
    for chunk in tqdm(chunks, desc="✨ 追加数据进度"):
        vector_db.add_documents([chunk])
    print("✅ 新数据已追加到向量数据库")

def setup_rag_pipeline(llm, retriever):
    """设置 RAG 查询管道"""
    print(" 初始化 RAG 处理...")
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def load_pdf_to_db(pdf_path, embedding, db_path):
    """加载 PDF 文档到向量数据库"""
    documents = load_pdf(pdf_path)
    chunks = split_text(documents)
    embedding = OllamaEmbeddings(model="shaw/dmeta-embedding-zh")
    vector_db = load_or_create_chroma_db(chunks, embedding, db_path)
    add_data_to_chroma_db(vector_db, chunks)

# 主程序
if __name__ == "__main__":
    pdf_path = "./spring-boot.pdf"
    db_path = "./chroma_db"

    embedding = OllamaEmbeddings(model="shaw/dmeta-embedding-zh")

    load_pdf_to_db(pdf_path, embedding, db_path)

    vector_db = Chroma(persist_directory=db_path, embedding_function=embedding)
    
    llm = Ollama(model="qwen2.5")
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    qa_chain = setup_rag_pipeline(llm, retriever)

    query = "PDF 里关于 GraalVM 说了什么？具体在哪几个章节提到了?"
    print(f" 正在查询: {query}")
    response = qa_chain.run(query)
    print(" 回答:", response)
