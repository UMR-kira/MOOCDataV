import pandas as pd
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from pyecharts.charts import WordCloud
from pyecharts.charts import Timeline

tl = Timeline()
timelist = ['2018-6', '2018-12', '2019-6', '2019-12', '2020-6',
            '2020-12', '2021-6', '2021-12', '2022-6', '2022-12']
for i in timelist:
    df = pd.read_csv('./words/' + i + '.csv', encoding='utf-8', header=None)
    data = df.values.tolist()
    tname = "基于评论数量的热门课程词云(" + i[:5] + str(eval(i[5:]) - 5) + "至" + i + ")"
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
        .add("", data, word_size_range=[20, 65], shape='pentagon')
        .set_global_opts(title_opts=opts.TitleOpts(title=tname, pos_left="center", pos_top="5%"))
        # .set_global_opts(title_opts=opts.TitleOpts("{}".format(tname)))
    )
    tl.add(wordcloud, "{}".format(i))

tl.render("timeline_multi_axis.html")
