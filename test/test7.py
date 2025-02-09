# pip install langchain chromadb pypdf ollama


from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain.llms import Ollama
from langchain.chains import RetrievalQA

# 1. 加载 PDF
pdf_path = "~/Downloads/spring-boot.pdf" # 替换为你的 PDF 路径
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# 2. 文本分割
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# 3. 加载 Ollama Embeddings
embedding = OllamaEmbeddings(model="llama3.2")  # 可替换成 "llama3.2" 或其他 Ollama 支持的模型

# 4. 存入 Chroma 向量数据库
vector_db = Chroma.from_documents(chunks, embedding, persist_directory="./chroma_db")
vector_db.persist()

# 5. 进行 RAG 查询
retriever = vector_db.as_retriever(search_kwargs={"k": 3})  # 取最相关的3条数据
llm = Ollama(model="llama3.2")  # 你可以换成 "gemma"、"llama3.2" 等
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 测试查询
query = "PDF 里关于 GraalVM 说了什么？"
response = qa_chain.run(query)
print("回答:", response)
