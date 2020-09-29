import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, Title
from bokeh.transform import jitter


def style_plots(fig):
    fig.background_fill_color = None
    fig.border_fill_color = None
    fig.toolbar.logo = None
    fig.toolbar_location = None
    fig.legend.background_fill_alpha = 0.3
    fig.outline_line_color = None
    fig.title.text_font_size = "11pt"
    fig.title.text_font_style = "bold"
    fig.title.text_color = "black"
    return fig


data_root = "clustering_output/"
jitter_amt = 0.08

# ballets = ["coppelia_dawn", "artifact", "raymonda", "sleepingbeauty_bluebird", "songs"]
ballets = ["raymonda", "coppelia_dawn", "artifact", "songs", "korobushka"]
colors = {"raymonda": "blue", "coppelia_dawn": "red", "artifact": "orange", "songs": "purple", "korobushka":"black"}
p = figure(plot_width=800, plot_height=600, title="Repetition and direction diversity indices")

for b in ballets:
    bbox_file = f"{data_root}{b}_indices.csv"
    df = pd.read_csv(bbox_file)
    df["color"] = colors[b]
    df["alpha"] = (df["measure_num"]-np.min(df["measure_num"]))/(np.max(df["measure_num"])-np.min(df["measure_num"]))

    # Plot clustering results
    # output_file(f"{b}_scatter_measure_movement_counts.html")
    source = ColumnDataSource(
        data=dict(
            # x=df["direction_diversity_index"],
            x=df["repetition_index"],
            y=df["repetition_index"],
            label=df["ballet"],
            col=df["color"],
            alpha=df["alpha"]
        )
    )
    # add a circle renderer with a size, color, and alpha
    p.circle(
        jitter("x", jitter_amt),
        jitter("y", jitter_amt),
        size=7,
        color="col",
        line_width=1,
        line_alpha=1,
        alpha="alpha",
        source=source,
        legend_group="label",
    )

p.xaxis.axis_label = "direction_diversity_index (DDI)"
p.yaxis.axis_label = "repetition_index (RI)"
p = style_plots(p)
p.legend.location = "top_right"
p.legend.click_policy = "hide"
p.add_layout(Title(text="Higher DDI, more diverse directional mvmt. Higher RI, more repetitive mvmt.", text_font_style="italic"), 'above')

# show the results
show(p)
