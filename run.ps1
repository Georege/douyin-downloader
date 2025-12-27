# 启动应用
# 获取脚本所在的目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -Path $scriptPath

# # 设置环境变量
# $env:FLASK_ENV = "pro"

# 激活虚拟环境
Set-ExecutionPolicy Bypass -Scope Process -Force
.\.venv\Scripts\Activate.ps1
Set-ExecutionPolicy RemoteSigned -Scope Process -Force

# 运行开发服务器
uv sync
uv run python downloader.py -c config.yml

# 暂停
Read-Host "Press Enter to continue..."
