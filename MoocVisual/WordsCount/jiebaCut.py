import jieba
import pandas as pd
txt = open("word.txt", "r", encoding='gbk').read()
words = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:
        continue
    else:
        counts[word] = counts.get(word, 0) + 1
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)
wordsdata = pd.DataFrame(items)
wordsdata.to_csv('wordsdata.csv', header=None, index=None)

