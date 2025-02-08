from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
from langchain.document_loaders import PyPDFLoader  # 导入 PyPDFLoader

# 1. 加载 PDF 文档
loader = PyPDFLoader("~/Downloads/spring-boot.pdf")  # 替换为你的 PDF 文件路径
documents = loader.load()

# 2. 创建 Embeddings 模型
embeddings = OllamaEmbeddings(model="llama3.2")  # 指定 Ollama 模型

# 3. 创建向量数据库
db = FAISS.from_documents(documents, embeddings)

# 4. 初始化 LLM
llm = Ollama(model="llama3.2")  # 指定 Ollama 模型

# 5. 创建 RAG 链
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())

# 6. 进行问答
query = "GraalVM 原生镜像讲的什么内容?"
result = qa.run(query)
print(result)
