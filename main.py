import asyncio
import httpx
from dataclasses import dataclass
API_URL = "https://api.github.com/search/repositories"
#定义数据类
@dataclass
class Repository:
    full_name:str
    stars:int
    url:str

async def search_repositories(keyword:str)->list[Repository]: #异步搜索函数
    params = {
        "q":keyword,
        "per_page":5,
    }
    #httpx 支持同步请求与异步请求
    #async with：自动管理客户端资源，代码块结束后自动关闭客户端
    async with httpx.AsyncClient(timeout=10) as client: #创建异步HTTP客户端
        response = await client.get(API_URL,params=params)
    response.raise_for_status()
    data = response.json()
    return [
        Repository(
            full_name=item['full_name'],
            stars = item['stargazers_count'],
            url = item['html_url']
            )
            for item in data['items']
    ] #列表推导式

async def main():
    keyword = input("请输入仓库搜索关键字：").strip()
    if not keyword:
        print('关键词不能为空')
        return 
    try:
        repositories = await search_repositories(keyword)#等待异步搜索完成并取得结果
    except httpx.HTTPError as error:
        print(f"请求失败:{error}")
        return 
    for repository in repositories:
        print(f'仓库:{repository.full_name}')
        print(f'星标数:{repository.stars}')
        print(f"链接：{repository.url}")
        print("-" * 40)

if __name__=='__main__':
    asyncio.run(main())