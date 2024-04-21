import jieba
import pandas as pd


def getKeyWords(txt, comment):
    words = jieba.lcut(txt, use_paddle=True)
    counts = {}
    for word in words:
        if len(word) < 3:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    wordsdata = pd.DataFrame(items).loc[:49]
    print("正在保存" + str(comment) + "评论的数据")
    wordsdata.to_csv('keywords of ' + str(comment) + '.csv', header=None, index=None)


def main():
    data = pd.read_csv("评论数据.csv", encoding='utf-8', index_col=0, header=None)
    dalist = data.values.tolist()
    good = ""
    bad = ""
    for info in dalist:
        if len(str(info[4])) > 100:
            if info[3] >= 4:
                good = good + str(info[4])
            elif info[3] <= 3:
                bad = bad + str(info[4])
        else:
            continue
    getKeyWords(good, "good")
    getKeyWords(bad, "bad")


main()
