# -*- coding: utf-8 -*-
"""top_harvard_data_api.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1lDnCKAO62lo14QebxrLzSishJpxop0oU
"""
# %%
from collections import defaultdict
import json
import pandas as pd
import numpy as np
from math import isnan
from flask import Flask, request, render_template, abort, jsonify
from flask_cors import CORS
# import dummy data

PER_PAGE = 10


def load_data():
    # import dummy data
    sheet_id = "1HFSAcEXK1K8vadOehu7Qf_DFoPrxBP4VCHnOYCPRKoI"

    sheet_tab_parameters = "dummy_parameters"
    sheet_tab_stats = "dummy_stats"
    sheet_tab_data = "dummy_data"

    parameters_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_parameters}"
    stats_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_stats}"
    data_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_tab_data}"

    parameters = pd.read_csv(parameters_url)
    stats = pd.read_csv(stats_url)
    data = pd.read_csv(data_url)

    data['county_code'] = data['county_code'].apply(
        lambda x: '{0:0>5}'.format(x))
    return parameters, stats, data


parameters, stats, data = load_data()
# %%


def get_factors():
    # get all parameters based on parameters table

    grouped_parameters = parameters.copy()
    grouped_parameters['category_grouped'] = list(
        zip(parameters.category, parameters.category_name))
    grouped_parameters['parameter_grouped'] = list(
        zip(parameters.parameter, parameters.parameter_name))
    grouped_parameters['option_grouped'] = list(
        zip(parameters.option, parameters.option_name))
    grouped_parameters.loc[pd.isna(
        grouped_parameters.option), 'option_grouped'] = np.nan

    factors = []
    for category, subdata in grouped_parameters.groupby(['category_grouped']):
        subfactors = []
        for parameter, subsubdata in subdata.groupby(['parameter_grouped']):
            subsubfactors = []
            for option, subsubsubdata in subsubdata.groupby(['option_grouped']):
                subsubfactors = subsubfactors + \
                    [{'name': option[0], 'text': option[1],
                        'param': subsubsubdata.data_variable.values[0]}]
            if len(subsubfactors) > 1:
                subfactors = subfactors + \
                    [{'name': parameter[0], 'text': parameter[1], 'sub': subsubfactors}]
            else:
                subfactors = subfactors + \
                    [{'name': parameter[0], 'text': parameter[1],
                        'param': subsubdata.data_variable.values[0]}]
        factors = factors + [{'name': category[0],
                              'text': category[1], 'sub': subfactors}]
    return json.dumps({"factors": factors})


# TEST /factors
# get_factors()

# %%


def get_parameters():
    # returns a lookup table for parameters
    parameters_dict = parameters.set_index('data_variable').to_dict('index')
    for param in parameters_dict.values():
        for k, v in param.items():
            try:
                if isnan(v):
                    param[k] = None
            except:
                pass
    return json.dumps(parameters_dict)


# TEST /parameters
# get_parameters()


# %%


def get_stats(county):
    # get all data for input county
    value_dict = data[data.county_code == county].to_dict('records')[0]

    grouped_stats = stats.copy()
    grouped_stats['category_grouped'] = list(
        zip(stats.category, stats.category_name))
    grouped_stats['parameter_grouped'] = list(
        zip(stats.parameter, stats.parameter_name))

    factors = []
    for category, subdata in grouped_stats.groupby(['category_grouped']):
        subfactors = []
        for parameter, subsubdata in subdata.groupby(['parameter_grouped']):
            subfactors = subfactors + [{'name': parameter[0],
                                        'text': parameter[1],
                                        'param': subsubdata.data_variable.values[0],
                                        'value': value_dict[subsubdata.data_variable.values[0]],
                                        'metric': subsubdata.metric.values[0]}]
        factors = factors + [{'name': category[0],
                              'text': category[1], 'sub': subfactors}]

    return json.dumps({"code": county, "stats": factors})

# TEST Testing
# json.loads(get_stats("01001"))


# %% All Counties


def get_counties():
    # get list of all country codes and all country names
    all_county_results = data[['county_code',
                               'county_name']].to_dict(orient='list')
    all_counties = {
        "all_counties": [
            {"code": code, "name": name} for [code, name] in zip(
                all_county_results["county_code"], all_county_results["county_name"]
            )
        ]
    }

    return json.dumps(all_counties)


# TEST Testing
# json.loads(get_counties())


# %%


def get_scores(args_dict):
    # calculate scores for all counties given input arguments
    def r(n): return lambda a: np.around(a, n)

    # prep for pagination
    pagination = False
    page = 0

    if "page" in args_dict:
        page = int(args_dict["page"])

        pagination = True
        args_dict = {k: v for k, v in args_dict.items() if k != "page"}

    # data processing
    vars = [x for x in args_dict if x+'_rank' in data.columns.values]
    rank_vars = [x+'_rank' for x in args_dict if x +
                 '_rank' in data.columns.values]

    ranks = data[rank_vars].values
    weights = pd.DataFrame([args_dict]).astype(int).transpose().values
    breakdowns = r(2)(ranks * np.transpose(weights) / weights.sum() * 100)

    # format code and name
    score_results = data[['county_code', 'county_name']].copy()
    score_results.rename(columns={'county_code': 'code',
                                  'county_name': 'name'}, inplace=True)

    # format coordinates
    score_results['lng_lat'] = (pd.Series(data[[
        'county_long', 'county_lat']]
        .to_dict('records'))
        .apply(lambda c: [c["county_long"], c["county_lat"]]))

    score_results['score'] = np.sum(breakdowns, axis=1)

    score_results[vars] = r(2)(ranks * 100)
    score_results['ranks'] = score_results[vars].to_dict('records')

    score_results = score_results.drop(vars, 1)

    score_results[vars] = breakdowns
    score_results['breakdown'] = score_results[vars].to_dict('records')
    score_results = score_results.drop(vars, 1)

    score_results = score_results.sort_values(
        'score', ascending=False)

    score_results = score_results.reset_index()
    score_results["ranking"] = score_results.index + 1

    score_results = score_results.to_dict('records')

    # infinite load and pagination logic
    if pagination:
        if page < 1:
            return ({"error": "page starts at 1"})
        end_i = page * PER_PAGE
        start_i = PER_PAGE * (page - 1)
        max_i = len(score_results)
        if end_i > max_i:
            if end_i - max_i < PER_PAGE:
                return json.dumps({"scores": score_results[start_i: max_i]})
            return {"error": "max_reached"}
        return json.dumps({"scores": score_results[start_i: end_i]})

    return json.dumps({"scores": score_results})


# TEST /scores
# get_scores({
#     "affordability_mortgage": 3,
#     "community_language_chinese": 3
# });

# %%


# create the flask app
app = Flask(__name__)
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})


@ app.route('/')
def return_index():
    return render_template('index.html')


@ app.route('/factors')
def return_factors():
    return get_factors()


@ app.route('/parameters')
def return_parameters():
    return get_parameters()


@ app.route('/scores')
def return_scores():
    return get_scores(request.args)


@ app.route('/stats')
def return_stats():
    return get_stats(request.args.get('county'))


@ app.route('/counties')
def return_counties():
    return get_counties()


if __name__ == '__main__':
    app.run()

# %%
