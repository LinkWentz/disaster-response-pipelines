# Imports.
import joblib
import json
import numpy as np
import os
import pandas as pd
import plotly
import re
import sqlite3 as sql
import sys
# Custom imports.
cwd = os.getcwd()

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../universal')
import universal_functions as uf

os.chdir(cwd)
# Flask imports.
from flask import Flask, render_template, request, jsonify
# Plotly imports.
from plotly.graph_objs import Bar

# Note that some imports are made solely to accomodate the model.

# Get arguments if provided.
if len(sys.argv) == 3:
    db_path, c_path = sys.argv[1:]
else:
    db_path = '../data/DisasterResponse.db'
    c_path = '../models/classifier.pkl'

app = Flask(__name__)

conn = sql.connect(db_path)
# Get main messages data.
df = pd.read_sql_query('SELECT * FROM categorized_messages', conn)
df.set_index('index', inplace = True)
# Get most common words series.
most_common_words = pd.read_sql_query('SELECT * FROM most_common_words', conn)
most_common_words.set_index('index', inplace = True)
most_common_words = most_common_words.iloc[:, 0]

conn.close()

# Create list of category names and the amount of messages in each.
dummy_columns = df.columns[5:]

cat_names = list(map(lambda txt : re.sub('_', ' ', txt).title(), dummy_columns))
messages_per_category = list(map(lambda cat : df[cat].sum(), dummy_columns))

# Load model.
model = joblib.load(c_path)

# Index webpage displays cool visuals and receives user input text for model.
@app.route('/')
@app.route('/index')
def index():
    # Save user input in query.
    query = request.args.get('query', '')
    # Get the predictions for each category.
    cat_values = model.predict([query])[0]
    # Associate the predictions with the category labels.
    category_tuples = list(zip(cat_names, messages_per_category, cat_values))
    category_dicts = list(map(lambda x : {'name':x[0],'count':x[1],'value':x[2]},
                              category_tuples))
    # Reshape list into table.
    category_table = []
    cats_per_row = 3
    for i in np.arange(0, len(cat_values), cats_per_row):
        category_table.append(category_dicts[i:i+cats_per_row])

    # Extract data needed for visuals.
    cat_count_counts = df.groupby('cat_count').count()['message']
    cat_count_labels = list(np.arange(0, 10))

    most_common_word_labels = list(map(lambda txt : txt.title() + '-',
                                       most_common_words.index))
    # Create visuals.
    graphs = [
        {
            'data': [
                Bar(
                    x = cat_count_labels,
                    y = cat_count_counts
                )
            ],

            'layout': {
                'title': 'Messages by Amount of Categories',
                'yaxis': {
                    'title': ''
                },
                'width':  500,
                'height': 500
            }
        },
        {
            'data': [
                Bar(
                    x = most_common_words,
                    y = most_common_word_labels,
                    orientation='h'
                )
            ],

            'layout': {
                'title': 'Most Commonly Used Words',
                'yaxis': {
                    'categoryorder':'total ascending'
                },
                'width':  500,
                'height': 500
            }
        }
    ]

    # Encode plotly graphs in JSON.
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # Render web page with plotly graphs.
    return render_template('master.html', ids=ids, query=query,
                           graphJSON=graphJSON, category_table=category_table)

def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
