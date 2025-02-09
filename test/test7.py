# pip install langchain chromadb pypdf ollama


from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# 1. 加载 PDF
pdf_path = "your_file.pdf"  # 替换为你的 PDF 路径
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# 2. 文本分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 3. 加载 Ollama Embeddings
embedding = OllamaEmbeddings(model="mistral")  # 可换成 "llama2"、"gemma" 等

# 4. 加载或创建 Chroma 向量数据库
db_path = "./chroma_db"  # 向量数据库存储路径

try:
    # 先尝试加载已有数据库
    vector_db = Chroma(persist_directory=db_path, embedding_function=embedding)
    print("加载现有向量数据库")
except:
    # 如果加载失败，则创建新的数据库
    vector_db = Chroma.from_documents(chunks, embedding, persist_directory=db_path)
    vector_db.persist()
    print("创建新的向量数据库")

# 5. 追加新数据（如果数据库已经存在）
vector_db.add_documents(chunks)
vector_db.persist()  # 持久化保存
print("新数据已追加到向量数据库")

# 6. 进行 RAG 查询
retriever = vector_db.as_retriever(search_kwargs={"k": 3})  # 取最相关的3条数据
llm = Ollama(model="mistral")  # 你可以换成 "gemma"、"llama2" 等
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 测试查询
query = "PDF 里关于 XXX 说了什么？"
response = qa_chain.run(query)
print("回答:", response)
