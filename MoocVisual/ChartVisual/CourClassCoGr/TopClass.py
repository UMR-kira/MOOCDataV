import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie

df = pd.read_csv('课程类别数量和均分.csv', index_col=0, encoding='GBK', header=None)
data = df.values.tolist()

c = (
    Pie()

    .add(
        "",
        [list(z) for z in zip(data[0], data[1])],
        radius=["20%", "50%"],
        center=["23%", "45%"],
        rosetype="area",
    )
    .add(
        "",
        [list(z) for z in zip(data[0], data[3])],
        radius=["5%", "50%"],
        center=["67%", "45%"],
        rosetype="radius",
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="各类别课程数量及各类别课程均分加权排行", pos_left="25%"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_right="1%", pos_top="5%", orient="vertical")
    )
    .render("pie_rosetype.html")
)
