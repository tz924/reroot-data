# reROOT data API

For pulling all relevant data for reROOT web app.

Based on colab notebook [here](https://colab.research.google.com/drive/1lDnCKAO62lo14QebxrLzSishJpxop0oU).

## `/factors`

Returns a list of all user input parameters. These are the parameters used to calculated the reROOT score.


### Illustrative response

```json
{
  "diversity": {
    "cultural": "diversity_cultural",
    "economic": "diversity_economic",
    "lgbt": "diversity_lgbt"
  },
  "environment": {
    "air": "environment_air",
    "noise": "environment_noise",
    "water": "environment_water"
  },
  "housing": {
    "mortgage": "housing_mortgage",
    "rent": "housing_rent"
  },
  "immigrant": {
    "language": {
      "arabic": "immigrant_language_arabic",
      "chinese": "immigrant_language_chinese",
      "other": "immigrant_language_other",
      "spanish": "immigrant_language_spanish"
    },
    "origin": {
      "china": "immigrant_origin_china",
      "india": "immigrant_origin_india",
      "mexico": "immigrant_origin_mexico",
      "other": "immigrant_origin_other"
    }
  },
  "opportunity": {
    "employment": "opportunity_employment",
    "population": {
      "high": "opportunity_population_high",
      "low": "opportunity_population_low",
      "medium": "opportunity_population_medium"
    }
  },
  "service": {
    "banking": "service_banking",
    "internet": "service_internet",
    "library": "service_library",
    "medical": "service_medical",
    "senior": "service_senior",
    "transportation": "service_transportation"
  },
  "tax": {
    "education": "tax_education",
    "other": "tax_other",
    "welfare": "tax_welfare"
  },
  "vote": {
    "local": "vote_local",
    "national": "vote_national"
  }
}
```

## `/scores`

Returns final reROOT score for all counties, as well as breakdown of the scores. All the breakdown variables will sum up to the score . 

Requires at least one of the parameter variables noted in /parameters. Requires a numeric integer that indicates relative importance: 
- 0 = not important (default)
- 1 = important
- 2 = very important 

For example:

```
/scores?immigrant_language_arabic=1&immigrant_language_chinese=2
```

### Illustrative response

```json
{
  "00001": {
    "score": 1.21,
    "immigrant_language_arabic": 0.39,
    "immigrant_language_chinese": 0.82
  },
  "00002": {
    "score": 1.48,
    "immigrant_language_arabic": 0.16,
    "immigrant_language_chinese": 1.32
  },
 ...
}
```

## `/counties`

Returns all relevant information for an individual or list of counties.

For example:

```
/counties?counties=00001,00002
```

### Illustrative response

```json
{
  "00001": {
    "county_name": "Autauga County, Alabama",
    "coordinates": [
      35.7,
      -108.7
    ],
    "county_details": {
      "diversity_cultural_index": 0.82,
      "diversity_economic_index": 0.54,
      ...
    },
    "rank_details": {
      "diversity_cultural_rank": 0.98,
      "diversity_economic_rank": 0.84,
      ...
    }
  ...
}
```

## `/all_counties`

Returns all county codes and county names.

### Illustrative response

```json
{
  "county_code": [
    "00001",
    "00002",
    ...
    ],
  "county_name": [
	"Autauga County, Alabama",
	"Baldwin County, Alabama",
	...]
 }
 ```
