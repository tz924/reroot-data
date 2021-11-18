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


def load_data():
    """
    import dummy data
    """
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

    data['county_code'] = data['county_code'].apply(
        lambda x: '{0:0>5}'.format(x))
    return parameters, features, data


parameters, features, data = load_data()


def grouped_to_dict(grouped):
    """
    helper function to convert table to nested dictionary
    """
    results = defaultdict(lambda: defaultdict(dict))

    for index, value in grouped.itertuples():
        index = tuple([x for x in index if not pd.isna(x)])
        for i, key in enumerate(index):
            if i == 0:
                nested = results[key]
            elif i == len(index) - 1:
                nested[key] = value
            else:
                nested = nested[key]

    return results


# create the flask app
app = Flask(__name__)


@app.route('/scores')
def scores():
    """
    calculate scores for all counties given input arguments
    """
    args_dict = request.args
    vars = [x for x in args_dict if x+'_rank' in data.columns.values]
    rank_vars = [x+'_rank' for x in args_dict if x +
                 '_rank' in data.columns.values]

    ranks = data[rank_vars].values
    weights = pd.DataFrame([args_dict]).astype(int).transpose().values

    score_results = data[['county_code']].copy()
    score_results['score'] = np.matmul(ranks, weights)
    score_results[vars] = ranks * np.transpose(weights)

    score_results = score_results.set_index('county_code').to_dict('index')

    return json.dumps(score_results)


@app.route('/counties')
def counties():
    """
    get all data for input counties
    """
    counties = request.args.get('counties')
    county_results = data[[
        str(x) in counties for x in data.county_code]].copy()

    county_results['coordinates'] = county_results[[
        'county_lat', 'county_long']].values.tolist()

    rank_detail_vars = [x for x in data.columns if '_rank' in x]
    county_results['rank_details'] = county_results[rank_detail_vars].to_dict(
        'records')

    county_detail_vars = [x for x in data.columns if ('_count' in x) | (
        '_median' in x) | ('_index' in x) | ('_percentage' in x)]
    county_results['county_details'] = county_results[county_detail_vars].to_dict(
        'records')

    county_results = county_results[[
        'county_code', 'county_name', 'coordinates', 'county_details', 'rank_details']]
    county_results = county_results.set_index(
        'county_code').transpose().to_dict()
    return json.dumps(county_results)


@app.route('/factors')
def factors():
    """
    get all parameters based on parameters table
    """
    grouped_data = parameters[['category',
                               'subcategory', 'field', 'variable_name']]
    grouped_data = grouped_data.groupby(
        ['category', 'subcategory', 'field'], dropna=False).agg(variable=('variable_name', 'max'))
    return json.dumps(grouped_to_dict(grouped_data))


@app.route('/all_counties')
def return_all_counties():
    """
    get list of all country codes and all country names
    """
    all_county_results = data[['county_code',
                               'county_name']].to_dict(orient='list')
    return json.dumps(all_county_results)


if __name__ == '__main__':
    app.run()
