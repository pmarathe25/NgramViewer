######################################################################################
# Pranav Marathe
# September 23, 2017
# This code creates a Bokeh webpage to display n-grams found in books from 2012 - 2016
######################################################################################

import os
import sys
import pickle
import random
import json
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, column, row
from bokeh.models.widgets import TextInput, Button, Dropdown
from autocorrect import spell
from vocabulary.vocabulary import Vocabulary as vb

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
                print "Loading %r..." % dataset
                year_data.append(pickle.load(f))
    return year_data

def spell_check(query):
    query_list = query.split()
    for index, q in enumerate(query_list):
        query_list[index] = spell(q.strip())
    suggestion = " ".join(query_list)
    return suggestion.strip()

def ngram_occurrences(query, data):
    degree = len(query.split()) - 1
    occurrences = []
    for year in data:
        occurrences.append(year[degree][0][query] / float(year[degree][1]))
    return occurrences

def generate_color(hex_length = 6):
    color = "#"
    for i in range(hex_length):
        color += str(random.choice("0123456789ABCDEF"))
    return color

def generate_synonym_list(query):
    synonym_list = []
    for word in query.split():
        syn = vb.synonym(word)
        if syn:
            syn = json.loads(syn)
            for synonym in syn:
                # Generate all the synonyms
                synonym_list.append(("Replace %s with %s" % (word, synonym['text']), word + " " + synonym['text']))
    return synonym_list

def synonym_handler():
    generate_synonyms.label = "Generating synonyms..."
    synonym_list = []
    for query in text_input.value.split(","):
        synonym_list.extend(generate_synonym_list(query.strip()))
    synonym_suggestions.menu = synonym_list
    generate_synonyms.label = "Done!"

def suggestion_handler():
    if spelling_suggestions.label.strip() != "":
        text_input.value = spelling_suggestions.label[13:-1].strip()

def text_input_handler(attr, old, new):
    global x_axis, year_data
    generate_synonyms.label = "Generate synonyms"
    # Generate outputs from all queries
    xs = []
    ys = []
    queries = []
    suggestion = ""
    for query in new.split(","):
        query = query.strip()
        if query != "":
            queries.append(query)
            suggestion += spell_check(query) + ", "
            y_axis = ngram_occurrences(query, year_data)
            # Now sort the axes in year-order
            x_axis, y_axis = (list(t) for t in zip(*sorted(zip(x_axis, y_axis))))
            xs.append(x_axis)
            ys.append(y_axis)
    # Update the plot
    spelling_suggestions.label = ("Did you mean %s?" % suggestion) if suggestion != new and suggestion[0:-1] != new and suggestion[0:-2] != new else ""
    source.data = {'xs': xs, 'ys': ys, 'labels': queries, 'colors': [generate_color() for q in queries]}

def replace_synonym(attr, old, new):
    word = synonym_suggestions.value.split()[0].strip()
    synonym = synonym_suggestions.value.split()[1].strip()
    text_input.value = text_input.value.replace(word, synonym)
    new_synonyms = []
    # This is a mess, but it works by replacing the word with the selected synonym in the dropdown menu.
    for index, elem in enumerate(synonym_suggestions.menu):
        # If this synonym is the selected one, swap it instead of replacing.
        if (synonym_suggestions.menu[index][1].split()[1] == synonym):
            new_synonyms.append( ("Replace %s with %s" % (synonym, word), synonym + " " + word) )
        else:
            new_synonyms.append( (synonym_suggestions.menu[index][0].replace(word, synonym), synonym_suggestions.menu[index][1].replace(word, synonym)) )
    synonym_suggestions.menu = new_synonyms

processed_dir = "processed/" if len(sys.argv) < 2 else sys.argv[1]
# Load all the pickle files.
year_data = load_data(processed_dir)
# Create the front-end
x_axis = [s.replace(".pkl", "") for s in os.listdir(processed_dir)]
# User Input
text_input = TextInput(value = "", title = "Graph these comma-separated phrases:")
text_input.on_change("value", text_input_handler)
# Spell check
spelling_suggestions = Button(label = "")
spelling_suggestions.on_click(suggestion_handler)
# Generate synonyms
generate_synonyms = Button(label = "Generate synonyms")
generate_synonyms.on_click(synonym_handler)
# Dropdown to select replacement synonyms
synonym_suggestions = Dropdown(label = "Synonyms", menu = [])
synonym_suggestions.on_change("value", replace_synonym)
# Plot!
p = figure(title = "Ngram Viewer", x_axis_label = 'Year', y_axis_label = 'Frequency', min_border = 75, plot_width = 900, plot_height = 700)
source = ColumnDataSource({'xs': [], 'ys': [], 'labels': [], 'colors': []})
p.multi_line('xs', 'ys', line_width = 2, color = 'colors', legend = 'labels', source = source)
# Show
curdoc().add_root(row(column(widgetbox(text_input, spelling_suggestions), p), widgetbox(generate_synonyms, synonym_suggestions)))
