import json
import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, Panel, Tabs, Band


def style_plots(fig, chart_width):
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
    fig.width = chart_width
    return fig

def make_trio_chart(
    df,
    chart_width,
    chart_height,
    line_color,
    bar_width,
    TOOLS,
    direction_movement_dict,
    body_movement_dict,
    height_movement_dict,
):
    trio_values = ["body_movement", "direction_movement", "height_movement"]
    row_list = []
    for val in trio_values:
        p = figure(
            plot_width=chart_width,
            plot_height=chart_height,
            tools=TOOLS,
        )
        source = ColumnDataSource(
            data=dict(
                x=dt,
                y=df_sub_region[col],
                rgn_text=df_sub_region[adm_colname],
                lower=df_sub_region_05[col],
                upper=df_sub_region_95[col],
            )
        )
        p.vbar()
        p = style_plots(p)
        row_list.append(p)
    return row(row_list)
