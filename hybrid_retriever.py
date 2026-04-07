from rank_bm25 import BM25Okapi
import jieba

class HybridRetriever:
    def __init__(self, collection):
        self.collection = collection
        self.bm25 = None
        self.documents = []
        
    def _build_bm25(self):
        """从ChromaDB加载所有文档构建BM25索引"""
        results = self.collection.get()
        if not results['documents']:
            return
        self.documents = results['documents']
        # 用jieba分词（支持中文）
        tokenized = [list(jieba.cut(doc)) for doc in self.documents]
        self.bm25 = BM25Okapi(tokenized)
        print(f"✅ BM25索引构建完成，共{len(self.documents)}个文档")
    
    def retrieve(self, query: str, n_results: int = 3) -> list:
        """混合检索：BM25 + 向量检索，结果合并去重"""
        
        # 1. 向量检索
        vector_results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        vector_docs = vector_results['documents'][0] if vector_results['documents'] else []
        
        # 2. BM25检索
        if self.bm25 is None:
            self._build_bm25()
            
        bm25_docs = []
        if self.bm25 and self.documents:
            tokens = list(jieba.cut(query))
            scores = self.bm25.get_scores(tokens)
            top_indices = sorted(range(len(scores)), 
                               key=lambda i: scores[i], reverse=True)[:n_results]
            bm25_docs = [self.documents[i] for i in top_indices]
        
        # 3. 合并去重
        combined = list(dict.fromkeys(vector_docs + bm25_docs))[:n_results]
        print(f"🔍 混合检索完成：向量{len(vector_docs)}条 + BM25{len(bm25_docs)}条 → 合并{len(combined)}条")
        
        return combined