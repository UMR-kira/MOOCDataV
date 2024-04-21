import pandas as pd
from pyecharts.globals import ThemeType
from pyecharts.charts import WordCloud
from pyecharts import options as opts

df = pd.read_csv('good.csv', encoding='GBK', header=None)
good = df.values.tolist()
df = pd.read_csv('bad.csv', encoding='GBK', header=None)
bad = df.values.tolist()
wordcloud1 = (
    WordCloud(init_opts=opts.InitOpts(theme=ThemeType.ROMA, width='1200'))
    .add("", good, word_size_range=[15, 40], shape='pentagon', pos_left="0%", width="600")
    .add("", bad, word_size_range=[15, 50], shape='pentagon', pos_left="36%", width="600")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="“优质与劣质”课程的区别--高低分评论对于课程评价标准", pos_left="22%", pos_top="10%"),
        legend_opts=opts.LegendOpts(pos_left="50%"),
    )
    .render("wordcloud.html")
)


