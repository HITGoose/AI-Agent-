from securag_engine import SecuRAG

bot = SecuRAG()

def llm_judge(question, answer, context):
    """用LLM评估RAG回答质量"""
    judge_prompt = f"""
    你是一个RAG系统评估专家。请评估以下回答的质量。
    
    问题：{question}
    检索到的上下文：{context}
    系统回答：{answer}
    
    请从两个维度打分（1-5分）：
    1. 相关性：回答是否基于上下文，没有编造
    2. 完整性：回答是否充分回答了问题
    
    只输出JSON格式：{{"relevance": 分数, "completeness": 分数, "reason": "简短理由"}}
    """
    response = bot.client.chat.completions.create(
        model=bot.model_name,
        messages=[{"role": "user", "content": judge_prompt}],
        temperature=0.0
    )
    return response.choices[0].message.content

# 测试用例
test_cases = [
    {
        "question": "什么是RAG？",
        "answer": "RAG是检索增强生成，结合检索和生成两个步骤。",
        "context": "RAG（Retrieval-Augmented Generation）是一种AI技术，通过检索相关文档来增强语言模型的生成能力。"
    },
    {
        "question": "transformer有什么优点？",
        "answer": "transformer支持并行计算，效果好。",
        "context": "Transformer架构通过自注意力机制实现并行计算，在NLP任务上取得了突破性进展。"
    }
]

for case in test_cases:
    result = llm_judge(case["question"], case["answer"], case["context"])
    print(f"问题：{case['question']}")
    print(f"评估结果：{result}\n")