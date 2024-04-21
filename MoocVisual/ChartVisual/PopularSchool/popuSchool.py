import pandas as pd
from pyecharts.charts import Bar3D
from pyecharts import options as opts

df = pd.read_csv('最受欢迎院校按总量.csv', index_col=0, encoding='GBK', header=0)
data = df.values.tolist()

data = [[d[1], d[2], d[3], d[0]] for d in data]
(
    Bar3D()
    .add(
        series_name='',
        label_opts=opts.LabelOpts(is_show=True, formatter=""),  # 就是不能单个输出value值
        data=data,
        # shading='realistic',
        xaxis3d_opts=opts.Axis3DOpts(type_="value", min_=0, max_=150, name='参与人数/万', name_gap=25),
        yaxis3d_opts=opts.Axis3DOpts(type_="value", min_=0, max_=7, interval=1, name='评论人数/万', name_gap=25),
        zaxis3d_opts=opts.Axis3DOpts(type_="value", min_=4.65, max_=4.83, interval=0.03, name='评论分数', name_gap=25),
        grid3d_opts=opts.Grid3DOpts(depth=100),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='最受"欢迎"的院校--依据参与人数，评论数和平均分', pos_left="center", pos_top="1%"),
        visualmap_opts=opts.VisualMapOpts(
            dimension=0,
            max_=150,
            pos_left="5%",
            pos_top="10%",
            range_color=[
                "#313695",
                "#4575b4",
                "#74add1",
                "#abd9e9",
                "#e0f3f8",
                "#ffffbf",
                "#fee090",
                "#fdae61",
                "#f46d43",
                "#d73027",
                "#a50026",
            ],
        ),
    )

    .render("bar3d_punch_card.html")
)
