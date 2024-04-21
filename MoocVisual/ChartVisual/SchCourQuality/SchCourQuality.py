import pandas as pd
from aiohttp import TCPConnector, ClientSession

import pyecharts.options as opts
from pyecharts.charts import Scatter3D


async def get_json_data(url: str) -> dict:
    async with ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url=url) as response:
            return await response.json()


df = pd.read_csv('院校开课质量排行.csv', encoding='GBK', header=0)
data = df.values.tolist()
data = [[d[4], d[2], d[3], d[1]] for d in data]

(
    Scatter3D()  # bg_color="black"
    .add(
        series_name="",
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(
            name='开课数',
            type_="value",
            min_=30,
            max_=180,
            interval=30,
            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name='精品课程数',
            type_="value",
            min_=20,
            max_=60,
            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name='国家精品率',
            type_="value",
            min_=0.1,
            max_=0.6,

            # textstyle_opts=opts.TextStyleOpts(color="#fff"),
        ),
        # grid3d_opts=opts.Grid3DOpts(width=90, height=80, depth=70),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title='课程最“优质”的院校--依据开课数，国家精品课程数及精品率', pos_left="center"),
        visualmap_opts=[
            opts.VisualMapOpts(
                type_="color",
                is_calculable=True,
                dimension=1,
                pos_top="10",
                pos_left="5%",
                max_=60,
                min_=20,
                range_color=[
                    "#1710c0",
                    "#0b9df0",
                    "#00fea8",
                    "#00ff0d",
                    "#f5f811",
                    "#f09a09",
                    "#fe0300",
                ],
            ),
            opts.VisualMapOpts(
                type_="size",
                is_calculable=True,
                dimension=0,
                pos_bottom="20",
                pos_left="5%",
                max_=180,
                range_size=[10, 50],
            ),
        ]
    )
    .render("scatter3d.html")
)
