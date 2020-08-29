import json
import pandas as pd

from bokeh.plotting import figure
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Panel, Tabs, Band


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

def make_trio_chart(
    df,
    chart_width,
    chart_height,
    line_color,
    bar_width,
    TOOLS
):
    direction_movement_df = df.direction_movement.value_counts()
    height_movement_df = df.height_movement.value_counts()
    body_movement_df = df.body_movement.value_counts()
    TOOLS = []
    p = figure(
        plot_width=chart_width,
        plot_height=chart_height,
        tools=TOOLS,
        x_range=list(direction_movement_df.index),
        title="Direction of movement",
    )
    source = ColumnDataSource(
        data=dict(
            x=list(direction_movement_df.index),
            y=list(direction_movement_df),
        )
    )
    p.vbar(
        x="x",
        top="y",
        width=bar_width,
        fill_color=line_color,
        source=source,
        line_width=0,
    )
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p = style_plots(p)
    p.xaxis.axis_label = "direction"
    p.yaxis.axis_label = "step count"

    p1 = figure(
        plot_width=250,
        plot_height=chart_height,
        tools=TOOLS,
        x_range=list(height_movement_df.index),
        title="Height of movement",
    )
    source = ColumnDataSource(
        data=dict(
            x=list(height_movement_df.index),
            y=list(height_movement_df),
        )
    )
    p1.vbar(
        x="x",
        top="y",
        width=bar_width,
        fill_color=line_color,
        source=source,
        line_width=0,
    )
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0
    p1 = style_plots(p1)
    p1.xaxis.axis_label = "height"
    p1.yaxis.axis_label = "step count"

    p2 = figure(
        plot_width=chart_width,
        plot_height=chart_height,
        tools=TOOLS,
        x_range=list(body_movement_df.index),
        title="Weight distribution",
    )
    source = ColumnDataSource(
        data=dict(
            x=list(body_movement_df.index),
            y=list(body_movement_df),
        )
    )
    p2.vbar(
        x="x",
        top="y",
        width=bar_width,
        fill_color=line_color,
        source=source,
        line_width=0,
    )
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0
    p2 = style_plots(p2)
    p2.xaxis.axis_label = "weight distribution"
    p2.yaxis.axis_label = "step count"
    return row(p1, p, p2)
