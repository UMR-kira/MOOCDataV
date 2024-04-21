import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

df = pd.read_csv('开课数量和次数.csv', encoding='GBK', index_col=0, header=None)
data = df.values.tolist()
bar1 = (
    Bar()
    .add_xaxis(data[0])
    .add_yaxis("开课次数", data[1])
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="门",
            type_="value",
            min_=100,
            max_=200,
            interval=10,
            axislabel_opts=opts.LabelOpts(formatter="{value} 门")
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="”最勤奋“的大学--基于开课数量和开课次数", pos_left="center"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="75%"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=35, interval=0)),
        yaxis_opts=opts.AxisOpts(
            name="开课次数",
            type_="value",
            min_=700,
            max_=1400,
            interval=100,
            axislabel_opts=opts.LabelOpts(formatter="{value} 次"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
    # .render("bar_base.html")
)
bar2 = (
    Bar()
    .add_xaxis(xaxis_data=data[0])
    .add_yaxis(
        series_name="开课总数",
        yaxis_index=1,
        y_axis=data[2],
        label_opts=opts.LabelOpts(is_show=True),
    )
)
bar1.overlap(bar2).render("bar_base.html")


