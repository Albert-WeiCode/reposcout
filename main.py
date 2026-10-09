import requests
from dataclasses import dataclass
API_URL = "https://api.github.com/search/repositories"
#定义数据类
@dataclass
class Repository:
    full_name:str
    stars:int
    url:str

def search_repositories(keyword:str)->list[Repository]:
    params = {
        "q":keyword,
        "per_page":5,
    }
    response = requests.get(API_URL,params=params,timeout = 10)
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
def main():
    keyword = input("请输入仓库搜索关键字：").strip()
    if not keyword:
        print('关键词不能为空')
        return 
    try:
        repositories = search_repositories(keyword)
    except requests.exceptions.RequestException as error:
        print(f"请求失败:{error}")
        return 
    for repository in repositories:
        print(f'仓库:{repository.full_name}')
        print(f'星标数:{repository.stars}')
        print(f"链接：{repository.url}")
        print("-" * 40)

if __name__=='__main__':
    main()