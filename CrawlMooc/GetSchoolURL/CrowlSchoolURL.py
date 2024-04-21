import pandas as pd
from bs4 import BeautifulSoup
mooc = open('../GetCourseURL/school.txt', 'r', encoding='utf-8')
soup = BeautifulSoup(mooc, 'html.parser')
# print(soup.prettify())
mooc.close()
data = []
data.append(["学校", "学校链接", "图片链接"])
schoolURL = pd.ExcelWriter("schoolURL.xlsx")  # 设置保存Excel 路径
for s in soup.find_all('a'):  # a标签循环迭代
    name = s.img.get('alt')
    link = s.get('href')
    img = s.img.get('src')
    url = 'https://www.icourse163.org' + link
    data.append([name, url, img])
data = pd.DataFrame(data)
data.to_excel(schoolURL, index=False)
schoolURL.save()

