from presidio_analyzer import AnalyzerEngine

# 1. 初始化引擎 (加载刚才下载的大模型，可能需要几秒钟)
print("⏳ 正在加载 AI 安全引擎，请稍候...")
analyzer = AnalyzerEngine()

def analyze_text(text: str):
    """
    使用 NLP 技术分析文本中的敏感实体
    """
    # 2. 让 AI 分析文本
    # language='en': 目前我们主要处理英文 (Dr. Wong 是全英教学)
    results = analyzer.analyze(text=text, language='en')
    
    # 3. 打印结果
    print(f"\n📄 原始文本: {text}")
    print("-" * 30)
    
    if not results:
        print("✅ 未发现敏感信息。")
        return

    print(f"🚨 发现 {len(results)} 个敏感信息风险:")
    for res in results:
        # res.entity_type: 敏感信息类型 (如 PERSON, PHONE_NUMBER)
        # res.score: AI 有多确信 (0-1.0)
        # start/end: 敏感词在字符串里的位置
        sensitive_word = text[res.start:res.end]
        print(f"  - [{res.entity_type}] \t: '{sensitive_word}' (置信度: {res.score:.2f})")

# --- 测试环节 ---
if __name__ == "__main__":
    # 这是一个没有固定格式的句子，正则搞不定的
    test_input = "HITGoose lives in Kuala Lumpur. His email is oj@monash.edu."
    
    analyze_text(test_input)
    
    print("\n" + "="*30)
    
    # 再测一个刚才的手机号
    analyze_text("Call me at 012-3456789 quickly!")

#今天的测试中发现这个手机号用Mircosoft presidio识别时候容易识别错误，因为NLP 是依赖于语境的
#所以我们此时如果使用正则表达式进行第一层机械化的过滤反而会提高精准度(对于手机号一类死板数据)