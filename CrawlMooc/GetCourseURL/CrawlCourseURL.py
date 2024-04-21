import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')


def getSchoolUrl():
    mooc = open('school.txt', 'r', encoding='utf-8')
    soup = BeautifulSoup(mooc, 'html.parser')
    mooc.close()
    ulist = []
    for s in soup.find_all('a'):
        link = s.get('href')
        url = 'https://www.icourse163.org' + link
        ulist.append(url)
    return ulist


def getCourseUrl(ulist, courseurl):  # 访问各学校链接获取课程链接
    web = webdriver.Chrome(options=chrome_options)
    courseurl.append(["school", "courseurl"])
    count = 0
    for link in ulist:  # 迭代每一个学校的链接
        # 获取总页数
        count = count + 1
        print("正在爬取第" + str(count) + "个学校的课程链接")
        try:
            schoolname = link[38:]  # 截取学校称号
            web.get(link + '#/c')
            time.sleep(2)
            pagehtml = web.page_source
            soup = BeautifulSoup(pagehtml, "html.parser")
            # 获得课程总页数
            sp = soup.find('a', attrs={"href": "#", "class": "zbtn znxt"})
            num = sp.previous_sibling
            pagenum = eval(num.get('class')[1][3:]) - 1
            # 末尾页的下一页标签情况 <a href="#" class="zbtn znxt" id="auto-id-1673638988923" one-link-mark="yes">下一页</a>
        except:
            continue

        # 获取所有课程链接
        try:
            while True:
                coursehtml = soup.find('div', attrs={"class": "um-spoc-course-list"})
                for curl in coursehtml.find_all('a', attrs={"target": "_blank"}):  # 获得所有链接
                    url = "https:" + curl.get('href')
                    courseurl.append([schoolname, url])
                if pagenum == 0:
                    break
                element = web.find_element(By.XPATH, '//*[@id="j-courses"]/div/div[2]/div/a[11]')  # 找到下一页的位置
                web.execute_script("arguments[0].click();", element)  # 切换下一页
                # 要找到的<a href="#" class="zbtn znxt js-disabled" id="auto-id-1673628679685" one-link-mark="yes">下一页</a>
                time.sleep(1)
                pagenum = pagenum - 1
                pagehtml = web.page_source
                soup = BeautifulSoup(pagehtml, "html.parser")  # 下一页数据
        except:
            continue

    web.close()
    return courseurl


def main():
    ulist = []
    ulist = getSchoolUrl()
    courseurl = []
    courseurl = getCourseUrl(ulist, courseurl)

    data = pd.ExcelWriter("courseurl.xlsx")
    courseurl = pd.DataFrame(courseurl)
    courseurl.to_excel(data, index=False)
    data.save()
    print("输出完毕")


main()
