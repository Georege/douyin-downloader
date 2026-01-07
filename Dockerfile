# https://uv.doczh.com/guides/integration/docker/

# ========== 阶段 1: 构建器 ==========
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim AS builder

WORKDIR /app

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装所有依赖 (--frozen 严格按照 uv.lock 安装)
RUN uv sync --frozen

# 复制应用代码
COPY . /app

# ========== 阶段 2: 运行 ==========
# https://uv.doczh.com/guides/integration/docker/
FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH" \
    TERM=xterm-256color \
    TZ=Asia/Shanghai

# 系统安装必要依赖
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org\/debian-security/mirrors.aliyun.com\/debian-security/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && \
    apt-get install -y curl gnupg ffmpeg tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# 设置工作目录
WORKDIR /app

# ✅ 从 builder 阶段复制虚拟环境
COPY --from=builder /app/.venv /app/.venv

# 复制应用代码
COPY . /app

# 创建必要的目录
RUN mkdir -p /app/Downloaded /app/logs


# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# 运行应用
CMD ["uv", "run", "python", "downloader.py", "--config", "config.yaml"]