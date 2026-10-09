# RepoScout

一个用于练习 Python HTTP 请求与异步编程的小项目。它可以并发搜索 GitHub 仓库，整理结果并去重。

## 功能

- 使用 HTTPX 和 asyncio 并发搜索多个关键词
- 返回仓库名称、星标数和 GitHub 链接
- 按仓库完整名称去重
- 提供可复用的 Github 搜索接口函数 `search_github_repositories`

## 环境准备

需要 Python 3.10 或更新版本。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt