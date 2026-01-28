import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from securag_engine import SecuRAG # 👈 引入我们昨天的引擎

def load_pdf_to_chroma(pdf_path):
    print(f"📄 正在读取文件: {pdf_path}")
    
    # 1. 读取 PDF 文本
    if not os.path.exists(pdf_path):
        print("❌ 文件不存在！请检查路径。")
        return

    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text()
        
    print(f"✅ 读取成功，共 {len(full_text)} 个字符。")
    
    # 2. 智能切片 (Chunking)
    # 这是 RAG 的核心技术之一：不能切断句子，要按语义切
    print("✂️ 正在进行文本切片...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,      # 每块约 500 字符
        chunk_overlap=50,    # 每块之间重叠 50 字 (防止切断上下文)
        separators=["\n\n", "\n", "。", ".", " ", ""] # 优先按段落切
    )
    
    chunks = text_splitter.split_text(full_text)
    print(f"🧩 共切分为 {len(chunks)} 个记忆片段。")
    
    # 3. 存入向量数据库
    print("🧠 正在唤醒 SecuRAG 引擎...")
    bot = SecuRAG() # 初始化引擎
    
    print("🚀 开始批量入库 (这可能需要一点时间)...")
    for i, chunk in enumerate(chunks):
        # 调用我们昨天写的 add_document 方法
        # 这里的 chunk 就是一段纯文本
        bot.add_document(doc_text=chunk)
        print(f"   - 片段 {i+1}/{len(chunks)} 已存入")
        
    print("🎉 入库完成！你的 AI 现在读过这本书了。")

if __name__ == "__main__":
    # 这里填你刚才放入 data 文件夹的文件名
    pdf_file = "./data/test.pdf" 
    
    load_pdf_to_chroma(pdf_file)