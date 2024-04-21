import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])


def getCourseInfo(courseurl):  # 获得所有课程信息
    outputcount = 0  # 链接总数为10254，变量控制输出次数为100次，每段输出103,末端46由程序报错退出
    for i in range(100):
        courseinfo = []
        commentsinfo = []
        courseinfo.append(["课程编号", "课程类别", "课程名称", "开课学校", "开课次数", "参加人数",
                           "课程评论数", "课程老师", "课程引言", "课程概述", "预备知识", "参考资料"])
        commentsinfo.append(["课程编号", "课程名称", "课程分数", "评论时间", "评论分数", "评论内容"])
        web = webdriver.Chrome(options=chrome_options)
        count = 0
        try:
            count = i * 103
            for url in courseurl[i * 103:(i + 1) * 103]:
                count = count + 1  # + i * 103 这样是错误的，因为他自增1，不需要额外加
                print("正在爬取第" + str(count) + "个课程链接：" + url[0])
                try:
                    web.get(url[0])
                    time.sleep(2)
                    html = web.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    # 课程ID
                    cid = url[0][34:]

                    try:  # 有极少数课程没有分类报错，在第98个文件位置，暂不考虑
                        # < a class ="breadcrumb_item sub-category" target="_blank" one-link-mark="yes" > 医药卫生 < / a >
                        cclass = soup.find('a', attrs={"class": "breadcrumb_item sub-category"}).string
                    except:
                        cclass = -1

                    # < span class ="course-title f-ib f-vam" > 骨骼肌肉系统再生医学 < / span >
                    cname = soup.find('span', attrs={"class": "course-title f-ib f-vam"}).string

                    # <a data-cate="课程介绍页" data-action="点击学校logo" data-label="-北京大学" ...</a>
                    cschool = soup.find('a', attrs={"data-cate": "课程介绍页"}).get('data-label')[1:]

                    try:  # 开课次数
                        # <span class="ux-dropdown_cnt th-fs0fc5 ux-btn-toggle">第16次开课 </span>
                        ccount = eval(re.findall(r'[1-9]\d*', soup.find('span', attrs={
                            "class": "ux-dropdown_cnt th-fs0fc5 ux-btn-toggle"}).string)[0])  # 匹配次数数字,超过一次开课
                    except:  # 找不到选择就是1次
                        ccount = 1

                    # <span class="count">已有 4334 人参加</span>
                    cpeople = eval(re.findall(r'[1-9]\d*', soup.find('span', attrs={"class": "count"}).string)[0])

                    # 获取课程老师
                    tnum = eval(re.findall(r'[1-9]\d*', soup.find('div', attrs={"class": "t-title f-fc3 f-f0"}).string)[
                                    0])  # 获取老师数量
                    pnum = int((tnum - 1) / 3)  # 页数
                    teachstr = ''
                    while True:  # 爬取老师
                        try:
                            teachlist = soup.find('div', attrs={"class": "um-list-slider_con"})
                            for teach in teachlist.findAll('img'):
                                teachstr = teachstr + teach.get('alt') + ' '

                            if pnum == 0:
                                break
                            # 找到下一页的位置  <span class="u-icon-arrow-right-thin f-ib f-pa"></span>
                            element = web.find_element(By.XPATH, "//*[@class='u-icon-arrow-right-thin f-ib f-pa']")
                            web.execute_script("arguments[0].click();", element)  # 切换下一页
                            time.sleep(0.3)
                            pnum = pnum - 1
                            pagehtml = web.page_source
                            soup = BeautifulSoup(pagehtml, "html.parser")  # 下一页数据
                        except:
                            print("爬取第" + str(count) + "个课程的老师出错")
                            break
                    cteacher = teachstr

                    # 获取评论数 <span id="review-tag-num">(10)</span>
                    try:
                        commnum = eval(soup.find('span', attrs={"id": "review-tag-num"}).string[1:-1])
                    except:  # 搜索不到则评论数为0
                        commnum = 0
                    # 获取课程引言
                    cguid = soup.find('div', attrs={"class": "course-heading-intro_intro"}).string

                    # 获取课程概述
                    csummary = soup.find('div', attrs={'class': "category-content j-cover-overflow"}).text

                    try:  # 预备知识，不一定有
                        cpreknow = soup.find('span', string="预备知识").parent.find_next_sibling().text
                    except:
                        cpreknow = ''
                    try:  # 参考资料，不一定有
                        crefer = soup.find('span', string="参考资料").parent.find_next_sibling().text
                    except:
                        crefer = ''

                    courseinfo.append([cid, cclass, cname, cschool, ccount, cpeople,
                                       commnum, cteacher, cguid, csummary, cpreknow, crefer])

                    # 爬取评论
                    if commnum:
                        pagenum = int((commnum - 1) / 20)  # 整除20+1就是页数，循环不用+1
                        element = web.find_element(By.XPATH, '//*[@id="review-tag-button"]')  # 找到评论区的位置
                        web.execute_script("arguments[0].click();", element)  # 切换评论区
                        time.sleep(1)
                        pagehtml = web.page_source
                        soup = BeautifulSoup(pagehtml, "html.parser")  # 评论区数据
                    else:  # 没有评论直接退出
                        continue
                    cp = 1  # 当前页数
                    pa = pagenum  # 总页数
                    try:  # 爬取课程分数
                        courgrade = eval(soup.find('div', attrs={
                            "class": "ux-mooc-comment-course-comment_head_rating-scores"}).span.string)
                    except:  # 评价人数不足
                        courgrade = -1  # getAverage()
                    while True:  # 爬取评论
                        print("正在爬取第" + str(cp) + "页的评论,总页数为" + str(pa + 1))
                        cp = cp + 1
                        try:
                            if pagenum:
                                element = web.find_element(By.LINK_TEXT, '下一页')  # 找到下一页的位置
                                web.execute_script("arguments[0].click();", element)  # 切换下一页
                                # times = time.perf_counter()
                                pagenum = pagenum - 1

                                commentslist = soup.findAll('div', attrs={"class": "ux-mooc-comment-course-comment_comment-list_item"})
                                for comment in commentslist:
                                    comtime = comment.find('div', attrs={'class': 'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'}).string[4:]
                                    comgrade = len(comment.find('div', attrs={"class": "star-point"}).findAll('i'))
                                    content = comment.find('div', attrs={'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'}).span.string
                                    commentsinfo.append([cid, cname, courgrade, comtime, comgrade, content])

                                time.sleep(0.9)
                                # timee = time.perf_counter()
                                # print("______ 时间是："+str(timee-times)+"_____")
                                pagehtml = web.page_source
                                soup = BeautifulSoup(pagehtml, "html.parser")  # 下一页数据
                            else:
                                commentslist = soup.findAll('div', attrs={"class": "ux-mooc-comment-course-comment_comment-list_item"})
                                for comment in commentslist:
                                    comtime = comment.find('div', attrs={'class': 'ux-mooc-comment-course-comment_comment-list_item_body_comment-info_time'}).string[4:]
                                    comgrade = len(comment.find('div', attrs={"class": "star-point"}).findAll('i'))
                                    content = comment.find('div', attrs={'class': 'ux-mooc-comment-course-comment_comment-list_item_body_content'}).span.string
                                    commentsinfo.append([cid, cname, courgrade, comtime, comgrade, content])
                                break
                        except:
                            print("爬取第" + str(pa + 1 - pagenum) + "页评论出错")
                            commentsinfo.append([cid, cname, (pa + 1 - pagenum), -1, -1, -1])  # 记录错误位置
                            break
                except:
                    print("爬取第" + str(count) + "个课程链接出错")
                    courseinfo.append([cid, -1, -1, -1, -1, -1,
                                       -1, -1, -1, -1, -1, -1])
        except:
            print('数组越界（到达末端链接）')
        web.close()
        outputFiles(courseinfo, commentsinfo, outputcount)
        outputcount = outputcount + 1
    return


def outputFiles(courseinfo, commentsinfo, outputcount):  # 输出信息到文件
    course = pd.ExcelWriter("./datainfo/CourseInfo_" + str(outputcount) + ".xlsx")
    courseinfo = pd.DataFrame(courseinfo)
    courseinfo.to_excel(course, index=False)
    course.save()
    comments = pd.ExcelWriter("./datainfo/CommentsInfo_" + str(outputcount) + ".xlsx")
    commentsinfo = pd.DataFrame(commentsinfo)
    commentsinfo.to_excel(comments, index=False)
    comments.save()


def main():
    url = pd.read_csv('courseurl.csv')
    courseurl = url.values.tolist()
    getCourseInfo(courseurl)


main()
