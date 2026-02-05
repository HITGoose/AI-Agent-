import re
from presidio_analyzer import AnalyzerEngine

class SecurityGuard:
    def __init__(self):
        # 🚫 黑名单：任何包含这些意图的词都会被拦截
        # 这种基于规则的拦截叫 "Deterministic Guardrails" (确定性护栏)
        print("🛡️ 加载安全组件...")
        self.analyzer = AnalyzerEngine()
        self.injection_patterns = [
            r"ignore all previous instructions",
            r"ignore the above instructions",
            r"you are now dan",  # 著名的 DAN 越狱模式
            r"you are now a pirate",
            r"system prompt",   # 防止套取系统设定
            r"simulated mode",
            r"dev mode",
            r"jailbreak"
        ]

    def check_injection(self, text: str) -> bool:
        """
        检查是否包含恶意注入指令
        返回: True (有攻击行为), False (安全)
        """
        text_lower = text.lower() # 转小写，防止大小写绕过
        
        for pattern in self.injection_patterns:
            # re.search 比 re.match 更强，只要句子里藏着这个词就能抓出来
            if re.search(pattern, text_lower):
                print(f"🚨 Security Alert: Detected injection attempt -> '{pattern}'")
                return True
        
        return False

    def _sanitize_input(self, text: str) -> str:
        """
        [私有方法] 第一道防线：正则 + 简单脱敏
        """
        # 1. 正则清洗 (Day 15 的逻辑)
        # 手机号
        text = re.sub(r"1[3-9]\d{9}", "[PHONE_REDACTED]", text)
        # 邮箱
        text = re.sub(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[EMAIL_REDACTED]", text)
        # 身份证
        text = re.sub(r"\d{17}[\dXx]|\d{15}", "[ID_REDACTED]", text)
        
        return text

    def _check_safety(self, text: str) -> bool:
        """
        [私有方法] 第二道防线：Presidio 智能检测
        返回 True 表示安全，False 表示有风险
        """
        # Day 16 的逻辑
        results = self.analyzer.analyze(text=text, language='en')
        
        # 如果发现有人名 (PERSON) 或 地名 (LOCATION)，不仅要拦截，最好报警
        for res in results:
            if res.score > 0.6: # 置信度大于 0.6
                print(f"🚨 [安全警报] 检测到敏感信息: {res.entity_type} (置信度 {res.score:.2f})")
                # 这里可以根据策略决定是否拦截，演示时我们只做警告
                # return False 
        return True
    
    