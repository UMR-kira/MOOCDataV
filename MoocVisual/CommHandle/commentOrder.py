import jieba
import pandas as pd


def getKeyWords(txt, year, month):
    words = jieba.lcut(txt, use_paddle=True)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    wordsdata = pd.DataFrame(items).loc[:29]
    print("正在保存第"+str(month)+"月的数据")
    wordsdata.to_csv(str(year)+'-'+str(month)+'.csv', header=None, index=None)


def main():
    year = 2018
    for i in range(5):
        filename = str(year) + ".csv"  # 要放在循环内部
        data = pd.read_csv(filename, encoding='utf-8', index_col=0, header=None)
        dalist = data.values.tolist()
        count = 1
        maxmouth = 6
        text = ''
        for items in dalist:
            mouth = eval(items[2].split('/')[1])
            if mouth <= maxmouth:
                text = text + str(items[0])
            else:
                getKeyWords(text, year, maxmouth)
                count = count + 1
                maxmouth = 6 * count
                text = ''
                continue
        getKeyWords(text, year, maxmouth)
        year = year + 1


main()
