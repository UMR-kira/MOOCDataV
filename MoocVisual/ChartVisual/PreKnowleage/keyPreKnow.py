import pandas as pd
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import WordCloud

df = pd.read_csv('先修知识词频.csv', encoding='GBK', header=None)
data = df.values.tolist()
wordcloud = (
    WordCloud(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
    .add("", data, word_size_range=[15, 65], shape='pentagon')
    .set_global_opts(title_opts=opts.TitleOpts(title="最需要先学的知识--先修知识词云", pos_left="center", pos_top="5%"))
    .render("wordcloud.html")
)

