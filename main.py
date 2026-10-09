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

async def main():
    raw_keywords = input("请输入仓库搜索关键字,多个关键字用逗号分隔：").strip()
    keywords = [part.strip()for part in raw_keywords.split(",") if part.strip()]
    if not keywords:
        print('关键词不能为空')
        return 
    try:
        #httpx 支持同步请求与异步请求
        #async with：自动管理客户端资源，代码块结束后自动关闭客户端
        async with httpx.AsyncClient(timeout=10) as client: #创建异步HTTP客户端
            #调用 async def函数 → 创建协程对象；通过 await 或 asyncio.gather() 等方式调度执行。
            tasks=[]
            for keyword in keywords:
                #await search_repositories(client, keyword) 直接执行并等待一个协程，不需要gather()
                tasks.append(search_repositories(client,keyword))
            results = await asyncio.gather(*tasks) #[[Repository()],Repository()],...]
    except httpx.HTTPError as error:
        print(f"请求失败:{error}")
        return 
    repositories = []  
    for result in results:
        repositories.extend(result) #添加元素进列表
    #repositories [[Repository()],Repository()],....]
    unique_repositories: dict[str, Repository] = {}  # 用仓库完整名称作为键，保存唯一仓库

    for repository in repositories:  # 遍历合并后的仓库列表
        unique_repositories[repository.full_name] = repository  # 同名仓库会覆盖，从而去重

    repositories = list(unique_repositories.values())  # 把字典中的仓库对象转回列表
    print(f"共找到 {len(repositories)} 个不重复仓库：")  # 打印去重后的数量

    for repository in repositories:  # 逐个输出仓库
        print(f"仓库：{repository.full_name}")  # 打印完整名称
        print(f"星标数：{repository.stars}")  # 打印星标数
        print(f"链接：{repository.url}")  # 打印仓库链接
        print("-" * 40)  # 打印分隔线
if __name__=='__main__':
    asyncio.run(main())