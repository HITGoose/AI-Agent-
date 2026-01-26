import chromadb
from chromadb.utils import embedding_functions

def run_memory_demo():
    print("🧠 正在初始化大脑记忆体 (ChromaDB)...")
    
    # 1. 创建一个内存里的数据库客户端
    # (数据存在内存里，程序关闭就没了，适合测试)
    client = chromadb.Client()
    
    # 2. 创建一个“文件夹” (Collection)
    # 就像 SQL 里的 Table
    collection = client.create_collection(name="my_knowledge_base")
    
    # 3. 准备要存入的文档 (模拟 PDF 切片后的内容)
    documents = [
        "HITGoose is an expert in AI Security and Watermarking.",  # 文档 1: 介绍 
        "Monash University Malaysia is located in Sunway City.",    # 文档 2: 介绍学校
        "Durian is the king of fruits, very popular in Malaysia.", # 文档 3: 介绍榴莲
        "RAG stands for Retrieval-Augmented Generation."           # 文档 4: 介绍技术
    ]
    
    # 4. 存入数据库 (自动向量化！)
    # Chroma 会自动调用内置模型，把这些英语句子变成一串串数字列表
    print(f"📥 正在存入 {len(documents)} 条记忆片段...")
    collection.add(
        documents=documents,
        ids=["doc1", "doc2", "doc3", "doc4"] # 每条数据要有唯一的身份证号
    )
    
    # --- 见证奇迹的时刻 ---
    
    # 5. 用户提问
    user_query = "Where is the campus?" 
    # 注意：文档里没有 "campus" 这个词，只有 "University" 和 "Sunway City"
    
    print(f"\n❓ 用户提问: '{user_query}'")
    print("🔍 正在大脑中检索最相关的记忆...")
    
    results = collection.query(
        query_texts=[user_query],
        n_results=1 # 只找最相似的 1 条
    )
    
    # 6. 展示结果
    best_match = results['documents'][0][0]
    print(f"✅ 找到最佳匹配: '{best_match}'")

if __name__ == "__main__":
    run_memory_demo()