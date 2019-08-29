import requests
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
url = 'https://www.zhipin.com'
urls = requests.get(url, headers=headers).text
soup = BeautifulSoup(urls, 'lxml')
print(soup)



# for i in soup.find_all('div', class_="job-primary"):
#     for y in i.find_all(class_="company-test"):
#         for q in y.find_all('h3'):
#             name.append(q.get_test())
#
#
# post = []
#
# for i in soup.find_all('div', class_="job_title"):
#     post.append(i.get_text())
#
# salary = []
#
# for i in soup.find_all('span', class_="red"):
#     salary.append(i.get_text())
#
# address = []
#
# for i in soup.find_all(class_="info-primary"):
#     for y in i.find_all('p'):
#         address.append(y.get_text())
# for q,w,e,r in zip(name,post,salary,address):
#     print("公司名字：",q)
#     print("岗位：",w,end='')
#     print("薪资：",e)
#     print("地址：",r)
#     print("-" * 20)