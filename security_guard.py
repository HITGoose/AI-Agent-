import re

class SecurityGuard:
    def __init__(self):
        # 🚫 黑名单：任何包含这些意图的词都会被拦截
        # 这种基于规则的拦截叫 "Deterministic Guardrails" (确定性护栏)
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

