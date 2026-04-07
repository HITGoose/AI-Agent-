from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self):
        print("🔄 加载Reranker模型...")
        # 这是一个轻量级的中英文reranking模型
        self.model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        print("✅ Reranker加载完成")
    
    def rerank(self, query: str, documents: list, top_k: int = 3) -> list:
        """
        对检索结果重新排序
        输入: 查询 + 文档列表
        输出: 重排后的top_k个文档
        """
        if not documents:
            return documents
            
        # 构建(query, doc)对
        pairs = [(query, doc) for doc in documents]
        
        # 打分
        scores = self.model.predict(pairs)
        
        # 按分数排序
        scored_docs = sorted(zip(scores, documents), reverse=True)
        
        top_docs = [doc for _, doc in scored_docs[:top_k]]
        print(f"✅ Reranking完成，从{len(documents)}个文档中选出top{top_k}")
        
        return top_docs