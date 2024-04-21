import pandas as pd
# EXCEL转化为CSV文件
for count in range(100):
    data = pd.read_excel("./datainfo/CommentsInfo_" + str(count) + ".xlsx", 'Sheet1', skiprows=[0, 1], index_col=0)
    path = "./data/Comments_" + str(count) + ".csv"
    data.to_csv(path, encoding='utf-8')

# CSV文件评论合并
for count in range(100):
    data = pd.read_csv("./data/Comments_" + str(count) + ".csv", index_col=0)
    data.to_csv('./comments.csv', encoding="utf_8_sig", header=False, mode='a+')

# 去重，提取出单个课程分数
data = pd.read_csv('comments.csv', encoding='utf_8_sig', index_col=False)
data.drop_duplicates(subset='A', keep='last', inplace=True)
data.to_csv('comcut.csv')

