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

async def search_repositories(
    client:httpx.AsyncClient,
    keyword:str)->list[Repository]: #异步搜索函数
    params = {
        "q":keyword,
        "per_page":5,
    }
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

async def search_github_repositories(
    keywords: list[str],  # 接收一个或多个搜索关键词
) -> list[dict[str, str | int]]:  # 返回可序列化的字典列表
    """并发搜索多个关键词，去重后返回仓库信息。"""  # 描述这个函数的用途

    if not keywords:  # 检查调用方是否传入了关键词
        return []  # 没有关键词时返回空列表

    async with httpx.AsyncClient(timeout=10) as client:  # 创建一个供所有查询共用的客户端
        tasks = []  # 准备保存每个关键词对应的搜索协程
        for keyword in keywords:  # 遍历所有关键词
            tasks.append(search_repositories(client, keyword))  # 创建一个搜索协程并保存
        result_groups = await asyncio.gather(*tasks)  # 并发执行所有搜索并收集结果

    unique: dict[str, Repository] = {}  # 用仓库完整名称作为键，保存不重复的仓库对象
    for group in result_groups:  # 遍历每个关键词对应的结果列表
        for repository in group:  # 遍历当前结果列表里的仓库
            unique[repository.full_name] = repository  # 用完整名称去重

    return [  # 开始构造最终返回值
        {  # 把每个仓库对象转换成普通字典
            "full_name": repository.full_name,  # 保存仓库完整名称
            "stars": repository.stars,  # 保存星标数量
            "url": repository.url,  # 保存仓库链接
        }
        for repository in unique.values()  # 遍历去重后的仓库
    ]

async def main():
    raw_keywords = input("请输入仓库搜索关键字,多个关键字用逗号分隔：").strip()
    keywords = [part.strip()for part in raw_keywords.split(",") if part.strip()]
    if not keywords: 
        print("关键词不能为空") 
        return  
    try:
        repositories = await search_github_repositories(keywords)
    except httpx.HTTPError as error:
        print(f"请求失败:{error}")
        return 
    print(len(repositories))
    for repository in repositories:  # 逐个输出仓库
        print(f"仓库：{repository['full_name']}")  # 打印仓库名称
        print(f"星标数：{repository['stars']}")  # 打印星标数量
        print(f"链接：{repository['url']}")  # 打印仓库链接
        print("-" * 40)  # 打印分隔线
if __name__=='__main__':
    asyncio.run(main())