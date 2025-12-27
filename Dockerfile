FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org\/debian-security/mirrors.aliyun.com\/debian-security/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y curl gnupg && \
    curl -sL https://deb.nodesource.com/setup_20.x  | bash - && \
    apt-get install -y nodejs

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

RUN apt-get update && \
    apt-get install -y ffmpeg tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

CMD ["python", "downloader.py", "--config"]