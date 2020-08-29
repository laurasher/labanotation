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
    fig.title.text_font_size = "10pt"
    fig.title.text_font_style = "normal"
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
@st.cache
def _get_data(dir):
    df = pd.read_csv(f"bbox_output/{dir}.csv")
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
chart_width = 400
chart_height = 350
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

### Generate plots & Put together layout
####################################################################################
# Movement direction
direction_movement_dict = [
    "place",
    "right",
    "left",
    "forward",
    "backward",
    "forward_diagonal",
    "backward_diagonal",
]
# Body motion
body_movement_dict = [
    "right_arm",
    "left_arm",
    "right_body",
    "left_body",
    "right_leg",
    "left_leg",
    "right_hand",
    "left_hand",
    "right_support",
    "left_support",
    "head",
]
# Movement height
height_movement_dict = ["low", "middle", "high"]

# Step length
source = ColumnDataSource(
    data={
        "x_values": [int(x) for x in df.index],
        "y_values": [int(x) for x in df.step_length],
        "labels": list(df.label),
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
    fill_color=line_color,
    source=source,
    line_width=0,
)
p.xgrid.grid_line_color = None
p.y_range.start = 0
p = style_plots(p)
p.xaxis.axis_label = "choreography order"
p.yaxis.axis_label = "step length"
st.bokeh_chart(p, use_container_width=True)

# trio_chart = make_trio_chart(
#     df,
#     chart_width,
#     chart_height,
#     line_color,
#     bar_width,
#     TOOLS,
#     direction_movement_dict,
#     body_movement_dict,
#     height_movement_dict,
# )
# st.bokeh_chart(trio_chart, use_container_width=True)
