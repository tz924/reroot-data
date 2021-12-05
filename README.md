# reROOT data API

For pulling all relevant data for reROOT web app.

Based on colab notebook [here](https://colab.research.google.com/drive/1lDnCKAO62lo14QebxrLzSishJpxop0oU).

## `/factors`

Returns a list of all user input parameters. These are the parameters used to calculated the reROOT score.

### Sample Response

```json
{
   "factors":[
      {
         "name":"affordability",
         "text":"AFFORDABILITY",
         "sub":[
            {
               "name":"mortgage",
               "text":"CHEAP MORTGAGE",
               "param":"affordability_mortgage"
            },
            {
               "name":"rent",
               "text":"CHEAP RENT",
               "param":"affordability_rent"
            }
         ]
      },
      ...
   ]
}
```

## `/parameters`

Returns a lookup table for parameters

For example:

```text
/parameters
```

### Sample Response

```json
{
   "affordability_mortgage":{
      "category_name":"AFFORDABILITY",
      "parameter_name":"CHEAP MORTGAGE",
      "option_name":"NaN",
      "category":"affordability",
      "parameter":"mortgage",
      "option":"NaN",
      "data_type":"int"
   },
  ...
}
```

## `/stats`

calculate scores for all counties given input arguments

For example:

```text
/stats?county=01001
```

### Sample Response

```json
{
  'code': '01001',
  'stats': [
    { 'name': 'community',
      'text': 'COMMUNITY',
      'sub': [{ 
        "name":"language",
        "text":"MULTILINGUAL",
        "param":"community_language_percentage",
        "value":0.3112,
        "metric":"percentage"
        },
      ...]
    },
    ...]
}
```

## `/counties`

Returns all county codes and county names.

### Sample Response

```json
{'all_counties': [
  {'code': '01001', 'name': 'Autauga County, AL'},
  {'code': '01003', 'name': 'Baldwin County, AL'},
  ...]}
 ```

## `/scores`

Returns final reROOT score for all counties, as well as breakdown of the scores,
in descending sorted order.
All the breakdown variables will sum up to the score.

Requires at least one of the parameter variables noted in /parameters. Requires a numeric integer that indicates relative importance:

- 0 = Not important at all(default)
- 1 = Not very important
- 2 = Somewhat important
- 3 = Very important
- 4 = Extremely important

For example:

```text
/scores?immigrant_language_arabic=1&immigrant_language_chinese=2
```

### Sample Response

```json
{
   "scores":[
      {
         "code":"08123",
         "name":"Weld County, CO",
         "lng_lat":[-104.4, 40.6],
         "score":0.9995225971,
         "ranks":{
            "affordability_mortgage":0.9996817314,
            "community_language_chinese":0.9993634628
         },
         "breakdown":{
            "affordability_mortgage":0.4998408657,
            "community_language_chinese":0.4996817314
         }
      },
 ...
}
```
