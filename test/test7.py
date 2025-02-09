from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from tqdm import tqdm  # 进度条库

# 1. 加载 PDF
pdf_path = "~/Downloads/spring-boot.pdf"  # 替换为你的 PDF 路径
print("📄 正在加载 PDF...")
loader = PyPDFLoader(pdf_path)
documents = loader.load()

# 2. 文本分割
print("📜 正在拆分文本...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = list(tqdm(text_splitter.split_documents(documents), desc="🔹 文本块处理"))

# 3. 加载 Ollama Embeddings（自动使用 GPU）
print("🧠 加载 Ollama Embeddings...")
embedding = OllamaEmbeddings(model="llama3.2")  # 可换成 "llama2"、"gemma" 等

# 4. 加载或创建 Chroma 向量数据库
db_path = "~/test/chroma_db"
try:
    print("📁 尝试加载现有向量数据库...")
    vector_db = Chroma(persist_directory=db_path, embedding_function=embedding)
    print("✅ 已加载现有向量数据库")
except:
    print("⚡ 创建新的向量数据库...")
    vector_db = Chroma.from_documents(chunks, embedding, persist_directory=db_path)
    vector_db.persist()
    print("✅ 新数据库创建完成")

# 5. 追加新数据（如果数据库已经存在）
print("📥 正在追加新数据到数据库...")
for chunk in tqdm(chunks, desc="✨ 追加数据进度"):
    vector_db.add_documents([chunk])
vector_db.persist()
print("✅ 新数据已追加到向量数据库")

# 6. 进行 RAG 查询（GPU 加速）
print("🤖 初始化 RAG 处理...")
llm = Ollama(model="llama3.2", num_gpu_layers=50)  # 让 Ollama 尽可能多使用 GPU
retriever = vector_db.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 测试查询
query = "PDF 里关于 GraalVM 说了什么？"
print(f"🔎 正在查询: {query}")
response = qa_chain.run(query)
print("💡 回答:", response)
