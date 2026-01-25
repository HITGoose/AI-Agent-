import requests
import json

url = "https://jsonplaceholder.typicode.com/posts/1"
print(f"正在连接: {url}")
response = requests.get(url)

print(f"状态码: {response.status_code}")

data = response.json()

print("收到的数据 (JSON):")
print(json.dumps(data, indent=4, ensure_ascii= False))

print(f"标题是: {data['title']}")