import json
from openai import OpenAI
import config
import tools

#初始化客户端,直接调用config里的配置
client = OpenAI(
    api_key = config.API_KEY,
    base_url = config.BASE_URL
)

def chat_loop():
    print("AI Agent 启动ing")
    print(f"已加载工具：{list(tools.tools_map.keys())}")#提取工具字典的键打包成列表输出
#初始化ai人设
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]

    while True:
        try:
            #用户输入环节
            user_input = input("\n User: ").strip()
            if user_input.lower() == "exit":
                print("再见")
                break
            messages.append({"role": "user", "content": user_input})#保存用户输入
            #把tools.tools.schema 传给AI，告诉他有什么工具用，让AI根据用户输入和可用工具决定下一步
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                tools=tools.tools_schema,#tool描述
                temperature=config.TEMPERATURE
            )
            #获取AI的回复消息对象
            ai_msg = response.choices[0].message
            #判断AI要不要调用工具？也就是返回的ai_msg中有没有含有tool_calls
            if ai_msg.tool_calls:
                #决定调用
                print(f"AI:我需要调用工具 -> {ai_msg.tool_calls[0].function.name}")
                #记住ai这个决定
                messages.append(ai_msg)

                #有时候ai会想一次调用2个工具，遍历一下
                for tool_call in ai_msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = tool_call.function.arguments
                    call_id = tool_call.id
                    #查找工具函数
                    if func_name in tools.tools_map:#名字在不在字典里
                        #1.获取相应函数名(菜名)，并通过func_name找到了负责这个函数的厨师tool_function先生(对于python来说此时tool_function就是对应找到的函数)
                        tool_function = tools.tools_map[func_name]
                        #2.解析参数，把AI传来的字符串变成PYthon能看懂的字典
                        args = json.loads(func_args)
                        #3.执行函数，将整理好的字典args加以解包，自动取出函数填入函数的参数内(也就是**的作用)，也因此能够做到各类问题通用，并丢给厨师tool_function先生，开炒！
                        tool_result = tool_function(**args)
                        #封装信息
                        messages.append({
                            "role": "tool", "tool_call_id": call_id, "content": tool_result
                        })
                    else:
                        print(f"错误：找不到工具{func_name}")
                
                #把工具交给ai，让他生成最终回复
                final_response = client.chat.completions.create(
                    model=config.MODEL_NAME,
                    messages=messages
                )
                #final_response (大盒子)
                    #└── choices (列表盒子)
                    #   └── [0] (第一个盒子)
                        #      └── message (消息盒子)
                        #         └── content (真正的文本) ✅
                final_content = final_response.choices[0].message.content#所以这里才要这样写，因为final_response里有很多信息
                print(f"AI:{final_content}")
                messages.append({"role": "assistant", "content": final_content})
            
            else:
                #ai不调用工具，聊天
                content = ai_msg.content
                print(f"AI: {content}")
                messages.append({"role": "assistant", "content": content})
        
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ =="__main__":
    chat_loop()

