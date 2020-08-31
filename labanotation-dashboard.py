import os
import json
import sys
import streamlit as st
import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column
from bokeh.models import ColumnDataSource

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from chart_trio import *

max_width_str = f"max-width: 98%;"
st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        {max_width_str}
        padding: 1rem 2rem 1rem 1rem;
    }}
    footer{{
        display: none;
    }}
    .modebar{{
        display: none;
    }}
</style>
""",
    unsafe_allow_html=True,
)


def style_plots(fig):
    fig.background_fill_color = None
    fig.border_fill_color = None
    fig.toolbar.logo = None
    fig.outline_line_color = None
    fig.title.text_font_size = "9pt"
    fig.title.text_font_style = "bold"
    fig.yaxis.major_label_text_color = "slategray"
    fig.xaxis.major_label_text_color = "slategray"
    fig.yaxis.major_tick_line_color = "slategray"
    fig.xaxis.major_tick_line_color = "slategray"
    fig.yaxis.minor_tick_line_color = "slategray"
    fig.xaxis.minor_tick_line_color = "slategray"
    fig.yaxis.axis_line_color = "slategray"
    fig.xaxis.axis_line_color = "slategray"
    fig.xaxis.major_label_text_font_size = "8pt"
    fig.yaxis.major_label_text_font_size = "8pt"
    return fig


###  Get data functions
####################################################################################
def _get_data(dir):
    df = pd.read_csv(f"bbox_output/{dir}.csv").drop(['Unnamed: 0'], axis=1).dropna()
    print(df)
    return df


def get_output_folders():
    files = [
        name.split(".csv")[0]
        for name in os.listdir("bbox_output/")
        if not ".DS_Store" in name
    ]
    print(f"Available output folders: {files}")
    return files


###  Styling params
####################################################################################
chart_width = 350
chart_height = 430
background_color = "#efeded"
line_width = 2
line_color = "slategray"
scatterdot_color = line_color
scatterdot_size = 3
bar_width = 0.4

html = """
  <style>
    /* 1st button */
    .stDeckGlJsonChart{
    }
    .streamlit-table.stTable{
    width: 20% !important;
    height: 40% !important;
    overflow: scroll !important;
    }
    div[data-baseweb="select"] {
        color: blue;
    }
  </style>
"""

TOOLS = "pan,reset,hover,save,box_zoom"
st.markdown(html, unsafe_allow_html=True)

### Get data
####################################################################################
output_files = get_output_folders()
output_select = st.sidebar.selectbox("Available labanotations", output_files)
df = _get_data(output_select)
color_field_select = st.sidebar.selectbox("Color field", ["movement body part","movement direction", "movement height"])
body_list = ['all','arm','leg','body','support','hand']
movement_body_select = st.sidebar.selectbox("Body movement", body_list)

### Generate plots & Put together layout
####################################################################################
# Step length
color_list = ['blue', 'red', 'orange', 'green', 'purple', 'gray', 'pink']
for i,b in enumerate(body_list[1:]):
    df.loc[df['body_movement'].str.contains(b), 'body_color'] = color_list[i]
    df.loc[df['body_movement'].str.contains(b), 'body_part'] = b
for i,b in enumerate(['high', 'middle', 'low']):
    df.loc[df['height_movement'].str.contains(b), 'height_color'] = color_list[i]
for i,b in enumerate(["place","right","left","forward","backward","forward_diagonal","backward_diagonal"]):
    df.loc[df['direction_movement'].str.contains(b), 'dir_color'] = color_list[i]

df_filt = df.dropna(subset=['body_movement'])
df_filt = df_filt[df_filt['body_movement'].str.contains(movement_body_select)]

if movement_body_select == 'all':
    df_filt = df

if color_field_select == 'movement body part':
    color_field = [x for x in df_filt.body_color]
    legend_field = list(df_filt.body_part)
if color_field_select == 'movement direction':
    color_field = [x for x in df_filt.dir_color]
    legend_field = list(df_filt.direction_movement)
if color_field_select == 'movement height':
    color_field = [x for x in df_filt.height_color]
    legend_field = list(df_filt.height_movement)

source = ColumnDataSource(
    data={
        "x_values": [int(x) for x in df_filt.index],
        "y_values": [int(x) for x in df_filt.step_length],
        "labels": list(df_filt.label),
        "color": color_field,
        "legend_field": legend_field
    }
)
TOOLTIPS = [
    ("labels", "@labels"),
]
p = figure(
    tools=TOOLS,
    plot_height=chart_height,
    plot_width=chart_width,
    title="Step length, ordered by choreography",
    tooltips=TOOLTIPS,
)
p.vbar(
    x="x_values",
    top="y_values",
    width=bar_width,
    fill_color="color",
    source=source,
    line_width=0,
    fill_alpha=0.8,
    legend_field="legend_field"
)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p = style_plots(p)
p.xaxis.axis_label = "choreography order"
p.yaxis.axis_label = "step length"
p.legend.orientation = "horizontal"
p.legend.location = "top_center"
st.bokeh_chart(p, use_container_width=True)

# Movement direction, weight distribution (body), height
trio_chart = make_trio_chart(
    df,
    670,
    chart_height,
    line_color,
    bar_width,
    TOOLS
)
st.bokeh_chart(trio_chart, use_container_width=False)
