import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType

df = pd.read_csv('最受欢迎课程.csv', encoding='GBK', header=None)
data = df.values.tolist()
bar = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
    .add_xaxis(xaxis_data=data[0])
    .add_yaxis(
        series_name="评论数",
        y_axis=data[2],
        label_opts=opts.LabelOpts(is_show=False),
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="人数",
            type_="value",
            min_=0,
            max_=330000,
            interval=30000,
            axislabel_opts=opts.LabelOpts(formatter="{value} 人"),
        )
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='最受"欢迎"的课程图--参与人数及评论数排行', pos_left="center"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="75%"),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger="axis", axis_pointer_type="cross"
        ),
        xaxis_opts=opts.AxisOpts(
            axislabel_opts=opts.LabelOpts(
                rotate=20,
                interval=0
            )
        ),
        yaxis_opts=opts.AxisOpts(
            name="评论数",
            type_="value",
            min_=0,
            max_=60000,
            interval=12000,
            axislabel_opts=opts.LabelOpts(formatter="{value} 条"),
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True),
        ),
    )
)
line = (
    Line()
    .add_xaxis(xaxis_data=data[0])
    .add_yaxis(
        series_name="参与人数",
        yaxis_index=1,
        y_axis=data[1],
        label_opts=opts.LabelOpts(is_show=True),
    )
)
bar.overlap(line).render("mixed_bar_and_line.html")
