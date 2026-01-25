from fastapi import  FastAPI
# 1.创建一个餐厅对象app
app = FastAPI()
# 2.挂招牌(路由)
# @app.get("/") 意思是当用户访问根路径(http://.../)，执行下面的函数
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI", "status": "开业大吉"}

# 3.再挂一个招牌(带参数的路径)
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "desc": "这是你点的菜"}