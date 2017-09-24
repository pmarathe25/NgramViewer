import os
import sys
import pickle
import random
from Tree import Tree
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import TextInput

def load_data(processed_dir):
    """
    Year data can be indexed as follows:

    count = data[year][n-gram degree][0][n-gram]
    total = data[year][n-gram degree][1]
    """
    year_data = []
    for dataset in [os.path.join(processed_dir, s) for s in os.listdir(processed_dir)]:
        if dataset[-3:] == "pkl":
            with open(dataset, 'rb') as f:
                year_data.append(pickle.load(f))
    return year_data

def ngram_occurrences(query, data):
    query_list = query.split()
    degree = len(query_list) - 1
    occurrences = []
    for year in data:
        print (year[0].get(query_list)).value
        print (year[0].get(query_list))
        occurrences.append(year[0].get(query_list).value / float(year[1][degree]))
    return occurrences

def generate_color(hex_length = 6):
    color = "#"
    for i in range(hex_length):
        color += str(random.choice("0123456789ABCDEF"))
    return color

def my_text_input_handler(attr, old, new):
    global x_axis, year_data, p
    # Generate outputs from all queries
    xs = []
    ys = []
    queries = []
    for query in new.split(","):
        query = query.strip()
        if query != "":
            queries.append(query)
            y_axis = ngram_occurrences(query, year_data)
            # Now sort the axes in year-order
            x_axis, y_axis = (list(t) for t in zip(*sorted(zip(x_axis, y_axis))))
            xs.append(x_axis)
            ys.append(y_axis)
    # Update the plot
    source.data = {'xs': xs, 'ys': ys, 'labels': queries, 'colors': [generate_color() for q in queries]}

processed_dir = "processed/" if len(sys.argv) < 2 else sys.argv[1]
# Load all the pickle files.
year_data = load_data(processed_dir)
# Create the front-end
x_axis = [s.replace(".pkl", "") for s in os.listdir(processed_dir)]
# User Input
text_input = TextInput(value = "", title = "Graph these comma-separated phrases:")
text_input.on_change("value", my_text_input_handler)
# Plot!
p = figure(title = "Ngram Viewer", x_axis_label = 'Year', y_axis_label = 'Frequency', min_border = 75, plot_width = 900, plot_height = 700)
source = ColumnDataSource({'xs': [], 'ys': [], 'labels': [], 'colors': []})
p.multi_line('xs', 'ys', line_width = 2, color = 'colors', legend = 'labels', source = source)
# Show
curdoc().add_root(column(widgetbox(text_input), p))
