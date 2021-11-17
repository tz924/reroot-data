# -*- coding: utf-8 -*-
"""top_harvard_data_api.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lDnCKAO62lo14QebxrLzSishJpxop0oU
"""

from collections import defaultdict
import json
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify


# import dummy data
sheet_id = "1HFSAcEXK1K8vadOehu7Qf_DFoPrxBP4VCHnOYCPRKoI"

sheet_tab_parameters = "dummy_parameters"
sheet_tab_features = "dummy_features"
sheet_tab_data = "dummy_data"

parameters_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_parameters}"
features_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_features}"
data_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_data}"

parameters = pd.read_csv(parameters_url)
features = pd.read_csv(features_url)
data = pd.read_csv(data_url)


def normalize_query_param(value):
    """
    Given a non-flattened query parameter value,
    and if the value is a list only containing 1 item,
    then the value is flattened.

    :param value: a value from a query parameter
    :return: a normalized query parameter value
    """
    return value if len(value) > 1 else value[0]


def normalize_query(params):
    """
    Converts query parameters from only containing one value for each parameter,
    to include parameters with multiple values as lists.

    :param params: a flask query parameters data structure
    :return: a dict of normalized query parameters
    """
    params_non_flat = params.to_dict(flat=False)
    return {k: normalize_query_param(v) for k, v in params_non_flat.items()}


def get_scores(request):
    """
    calculate scores for all counties given input arguments
    """
    parameter_vars = [x for x in request if request[x]]
    rank_vars = [x.replace("input_", "rank_") for x in parameter_vars]
    vars = [x.replace("input_", "") for x in parameter_vars]

    ranks = data[rank_vars].values
    weights = pd.DataFrame([request]).astype(int).transpose().values

    score_results = data[['county_code',
                          'county_lat', 'county_long']+rank_vars].copy()
    score_results['score'] = np.matmul(ranks, weights)
    score_results = score_results.sort_values(
        'score', ascending=False).to_dict('records')

    return json.dumps(score_results)


# get all data for input counties
def get_counties(request):
    counties = request.get('counties')
    county_results = data[[str(x) in counties for x in data.county_code]]
    county_results = county_results.set_index(
        'county_code').transpose().to_dict()
    return jsonify(county_results)


# helper function to convert table to nested dictionary
def grouped_to_dict(grouped):
    results = defaultdict(lambda: defaultdict(dict))

    for index, value in grouped.itertuples():
        for i, key in enumerate(index):
            if i == 0:
                nested = results[key]
            elif i == len(index) - 1:
                nested[key] = value
            else:
                nested = nested[key]

    return results


# get all parameters based on parameters table
def get_parameters():
    grouped_data = parameters[['category',
                               'subcategory', 'field', 'variable_name']]
    grouped_data = grouped_data.groupby(['category', 'subcategory', 'field']).agg(
        variable=('variable_name', 'max'))
    return json.dumps(grouped_to_dict(grouped_data))


# get list of all country codes and all country names
def get_all_counties():
    all_county_results = data[['county_code',
                               'county_name']].to_dict(orient='list')
    return json.dumps(all_county_results)


# create the flask app
app = Flask(__name__)


@app.route('/scores')
def return_scores():
    return get_scores(request.args)


@app.route('/counties')
def return_counties():
    return get_counties(request.args)


@app.route('/parameters')
def return_parameters():
    return get_parameters()


@app.route('/all_counties')
def return_all_counties():
    return get_all_counties()


if __name__ == '__main__':
    app.run()
