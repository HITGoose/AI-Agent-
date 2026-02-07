# 1. 使用官方 Python 3.10 轻量版作为基础镜像
FROM python:3.10-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 复制依赖清单并安装
# (这样做利用了 Docker 缓存机制，依赖不改动时不需要重新下载)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 复制当前目录下的所有代码到容器里
COPY . .

# 5. 声明我们需要暴露的端口
# 8000 是后端，8501 是前端
EXPOSE 8000
EXPOSE 8501

# 6. 设置环境变量 (解决 Python 输出缓冲问题)
ENV PYTHONUNBUFFERED=1

# 7. 默认命令 (会被 docker-compose 覆盖，这里写个占位)
CMD ["python", "api_server.py"]