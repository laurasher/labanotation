import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource

def style_plots(fig):
    fig.background_fill_color = None
    fig.border_fill_color = None
    fig.toolbar.logo = None
    fig.toolbar_location = None
    # fig.legend.background_fill_alpha = 0.3
    fig.outline_line_color = None
    fig.title.text_font_size = "9pt"
    fig.title.text_font_style = "bold"
    fig.title.text_color = "#394d7e"
    return fig


data_root = "clustering_output/"

# ballets = ["coppelia_dawn", "artifact", "raymonda", "sleepingbeauty_bluebird"]
ballets = ["raymonda","coppelia_dawn"]
colors = {
    'raymonda':'blue',
    'coppelia_dawn':'red',
}
p = figure(plot_width=600, plot_height=600)

for b in ballets:
    bbox_file = f"{data_root}{b}_indices.csv"
    df = pd.read_csv(bbox_file)
    df["color"] = colors[b]

    # Plot clustering results
    # output_file(f"{b}_scatter_measure_movement_counts.html")
    source = ColumnDataSource(
        data=dict(
            x=df["direction_diversity_index"],
            y=df["repetition_index"],
            label=df["ballet"],
            col=df["color"],
        )
    )
    # add a circle renderer with a size, color, and alpha
    p.circle("x", "y", size=7, color="col", alpha=0.8, source=source)
    p.xaxis.axis_label = "direction_diversity_index"
    p.xaxis.axis_label = "repetition_index"
    p = style_plots(p)

# show the results
show(p)

