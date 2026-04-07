from securag_engine import SecuRAG

bot = SecuRAG()

test_cases = [
    {"query": "AMOGEL模型的准确率是多少", "expected": "SEARCH"},
    {"query": "transformer的注意力机制是什么", "expected": "SEARCH"},
    {"query": "RAG和finetune有什么区别", "expected": "SEARCH"},
    {"query": "这篇论文的实验结果如何", "expected": "SEARCH"},
    {"query": "它的参数量是多少", "expected": "SEARCH"},
    {"query": "这个方法的局限性是什么", "expected": "SEARCH"},
    {"query": "论文里提到的数据集叫什么", "expected": "SEARCH"},
    {"query": "baseline模型是什么", "expected": "SEARCH"},
    {"query": "实验用了哪些评估指标", "expected": "SEARCH"},
    {"query": "这个模型在哪个任务上表现最好", "expected": "SEARCH"},
    {"query": "你好", "expected": "CHAT"},
    {"query": "帮我写一段Python冒泡排序", "expected": "CHAT"},
    {"query": "今天天气怎么样", "expected": "CHAT"},
    {"query": "讲个笑话", "expected": "CHAT"},
    {"query": "什么是机器学习", "expected": "CHAT"},
    {"query": "帮我翻译这句话：hello world", "expected": "CHAT"},
    {"query": "你是谁", "expected": "CHAT"},
    {"query": "1+1等于多少", "expected": "CHAT"},
    {"query": "帮我写个邮件模板", "expected": "CHAT"},
    {"query": "推荐几本AI书籍", "expected": "CHAT"},
]

correct = 0
for case in test_cases:
    result = bot._decide_intent(case["query"])
    is_correct = result == case["expected"]
    if is_correct:
        correct += 1
    print(f"{'✅' if is_correct else '❌'} [{case['expected']}→{result}] {case['query']}")

print(f"\n准确率: {correct}/20 = {correct/20*100:.0f}%")