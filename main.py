import requests
API_URL = "https://api.github.com/search/repositories"

def search_repositories(keyword):
    params = {
        "q":keyword,
        "per_page":5,
    }
    response = requests.get(API_URL,params=params,timeout = 10)
    response.raise_for_status()
    data = response.json()
    return data["items"]
def main():
    keyword = input("请输入仓库搜索关键字：").strip()
    try:
        repositories = search_repositories(keyword)
    except requests.exceptions.RequestException as error:
        print(f"请求失败:{error}")
        return 
    for repository in repositories:
        print(f'仓库:{repository["full_name"]}')
        print(f'星标数:{repository['stargazers_count']}')
        print(f"链接：{repository['html_url']}")
        print("-" * 40)

if __name__=='__main__':
    main()