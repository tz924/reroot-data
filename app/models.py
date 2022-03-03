#!/usr/bin/python3

import psycopg2
import pandas as pd


PARAMETER_SQL = """
SELECT category_name, parameter_name, option_name, category, parameter, option, data_variable, data_type FROM parameters;
"""

STATS_SQL = """
SELECT category_name, parameter_name, display_format, category, parameter, metric, data_variable, data_type FROM stats;
"""

COUNTY_DATA_SQL = """
SELECT county_code, county_name, county_lat, county_long, affordability_rent_rank, affordability_mortgage_rank, opportunity_employment_rank, opportunity_population_rank, 
community_cultural_rank, community_economic_rank, community_lgbt_rank, community_language_amharic_rank, community_language_arabic_rank, community_language_armenian_rank, 
community_language_bengali_rank, community_language_chinese_rank, community_language_french_rank, community_language_german_rank, community_language_greek_rank, 
community_language_gujarati_rank, community_language_haitian_rank, community_language_hebrew_rank, community_language_hindi_rank, community_language_italian_rank, 
community_language_japanese_rank, community_language_khmer_rank, community_language_korean_rank, community_language_malayalam_rank, community_language_navajo_rank, 
community_language_nepali_rank, community_language_other_rank, community_language_persian_rank, community_language_polish_rank, community_language_portuguese_rank, 
community_language_punjabi_rank, community_language_russian_rank, community_language_serbo_croatian_rank, community_language_spanish_rank, community_language_swahili_rank, 
community_language_tagalog_rank, community_language_tamil_rank, community_language_telugu_rank, community_language_thai_rank, community_language_ukrainian_rank, 
community_language_urdu_rank, community_language_vietnamese_rank, community_language_yiddish_rank, community_language_yoruba_rank, community_origin_afghanistan_rank, 
community_origin_albania_rank, community_origin_argentina_rank, community_origin_armenia_rank, community_origin_australia_rank, community_origin_austria_rank, 
community_origin_bahamas_rank, community_origin_bangladesh_rank, community_origin_barbados_rank, community_origin_belarus_rank, community_origin_belgium_rank, 
community_origin_belize_rank, community_origin_bolivia_rank, community_origin_bosnia_and_herzegovina_rank, community_origin_brazil_rank, community_origin_bulgaria_rank, 
community_origin_burma_rank, community_origin_cabo_verde_rank, community_origin_cambodia_rank, community_origin_cameroon_rank, community_origin_canada_rank, 
community_origin_caribbean_rank, community_origin_central_america_rank, community_origin_chile_rank, community_origin_china_rank, community_origin_colombia_rank, 
community_origin_congo_rank, community_origin_costa_rica_rank, community_origin_croatia_rank, community_origin_cuba_rank, community_origin_czechoslovakia_rank, 
community_origin_democratic_republic_of_congo_rank, community_origin_denmark_rank, community_origin_dominica_rank, community_origin_dominican_republic_rank, 
community_origin_ecuador_rank, community_origin_egypt_rank, community_origin_el_salvador_rank, community_origin_eritrea_rank, community_origin_ethiopia_rank, 
community_origin_france_rank, community_origin_germany_rank, community_origin_ghana_rank, community_origin_greece_rank, community_origin_grenada_rank, 
community_origin_guatemala_rank, community_origin_guyana_rank, community_origin_haiti_rank, community_origin_honduras_rank, community_origin_hungary_rank, 
community_origin_india_rank, community_origin_indonesia_rank, community_origin_iran_rank, community_origin_iraq_rank, community_origin_ireland_rank, community_origin_israel_rank, 
community_origin_italy_rank, community_origin_jamaica_rank, community_origin_japan_rank, community_origin_jordan_rank, community_origin_kazakhstan_rank, 
community_origin_kenya_rank, community_origin_korea_rank, community_origin_kuwait_rank, community_origin_laos_rank, community_origin_latvia_rank, community_origin_lebanon_rank, 
community_origin_liberia_rank, community_origin_lithuania_rank, community_origin_malaysia_rank, community_origin_mexico_rank, community_origin_moldova_rank, 
community_origin_morocco_rank, community_origin_nepal_rank, community_origin_netherlands_rank, community_origin_nicaragua_rank, community_origin_nigeria_rank, 
community_origin_north_macedonia_rank, community_origin_norway_rank, community_origin_other_rank, community_origin_pakistan_rank, community_origin_panama_rank, 
community_origin_peru_rank, community_origin_philippines_rank, community_origin_poland_rank, community_origin_portugal_rank, community_origin_romania_rank, 
community_origin_russia_rank, community_origin_saudi_arabia_rank, community_origin_senegal_rank, community_origin_serbia_rank, community_origin_sierra_leone_rank, 
community_origin_singapore_rank, community_origin_somalia_rank, community_origin_south_africa_rank, community_origin_south_america_rank, community_origin_spain_rank, 
community_origin_sri_lanka_rank, community_origin_st_vincent_and_the_grenadines_rank, community_origin_sudan_rank, community_origin_sweden_rank, community_origin_switzerland_rank, 
community_origin_syria_rank, community_origin_thailand_rank, community_origin_total_rank, community_origin_trinidad_and_tobago_rank, community_origin_turkey_rank, 
community_origin_uganda_rank, community_origin_ukraine_rank, community_origin_united_kingdom_rank, community_origin_uruguay_rank, community_origin_uzbekistan_rank, 
community_origin_venezuela_rank, community_origin_vietnam_rank, community_origin_west_indies_rank, community_origin_yemen_rank, community_origin_zimbabwe_rank, 
environment_air_rank, environment_water_rank, environment_land_rank, environment_build_rank, vote_local_rank, vote_national_rank, tax_education_rank, tax_health_rank, 
tax_welfare_rank, housing_rent_median, housing_mortgage_median, community_language_percentage, community_origin_percentage, community_lgbt_percentage, diversity_cultural_index, 
diversity_economic_index, environment_air_index, environment_water_index, environment_land_index, environment_build_index, opportunity_population_count, 
opportunity_population_density, opportunity_employment_percentage, tax_education_percentage, tax_health_percentage, tax_welfare_percentage, vote_local_index, vote_national_index 
FROM county_data;
"""

PARAMETERS_HEADER = ['category_name', 'parameter_name', 'option_name', 'category', 'parameter', 'option', 'data_variable', 'data_type']

STATS_HEADER = ['category_name', 'parameter_name', 'display_format', 'category', 'parameter', 'metric', 'data_variable', 'data_type']

COUNTY_DATA_HEADER = [
    'county_code', 'county_name', 'county_lat', 'county_long', 'affordability_rent_rank', 'affordability_mortgage_rank', 'opportunity_employment_rank', 
    'opportunity_population_rank', 'community_cultural_rank', 'community_economic_rank', 'community_lgbt_rank', 'community_language_amharic_rank', 
    'community_language_arabic_rank', 'community_language_armenian_rank', 'community_language_bengali_rank', 'community_language_chinese_rank', 
    'community_language_french_rank', 'community_language_german_rank', 'community_language_greek_rank', 'community_language_gujarati_rank', 
    'community_language_haitian_rank', 'community_language_hebrew_rank', 'community_language_hindi_rank', 'community_language_italian_rank', 'community_language_japanese_rank', 
    'community_language_khmer_rank', 'community_language_korean_rank', 'community_language_malayalam_rank', 'community_language_navajo_rank', 'community_language_nepali_rank', 
    'community_language_other_rank', 'community_language_persian_rank', 'community_language_polish_rank', 'community_language_portuguese_rank', 'community_language_punjabi_rank', 
    'community_language_russian_rank', 'community_language_serbo_croatian_rank', 'community_language_spanish_rank', 'community_language_swahili_rank', 
    'community_language_tagalog_rank', 'community_language_tamil_rank', 'community_language_telugu_rank', 'community_language_thai_rank', 'community_language_ukrainian_rank', 
    'community_language_urdu_rank', 'community_language_vietnamese_rank', 'community_language_yiddish_rank', 'community_language_yoruba_rank', 'community_origin_afghanistan_rank', 
    'community_origin_albania_rank', 'community_origin_argentina_rank', 'community_origin_armenia_rank', 'community_origin_australia_rank', 'community_origin_austria_rank', 
    'community_origin_bahamas_rank', 'community_origin_bangladesh_rank', 'community_origin_barbados_rank', 'community_origin_belarus_rank', 'community_origin_belgium_rank', 
    'community_origin_belize_rank', 'community_origin_bolivia_rank', 'community_origin_bosnia_and_herzegovina_rank', 'community_origin_brazil_rank', 
    'community_origin_bulgaria_rank', 'community_origin_burma_rank', 'community_origin_cabo_verde_rank', 'community_origin_cambodia_rank', 'community_origin_cameroon_rank', 
    'community_origin_canada_rank', 'community_origin_caribbean_rank', 'community_origin_central_america_rank', 'community_origin_chile_rank', 'community_origin_china_rank', 
    'community_origin_colombia_rank', 'community_origin_congo_rank', 'community_origin_costa_rica_rank', 'community_origin_croatia_rank', 'community_origin_cuba_rank', 
    'community_origin_czechoslovakia_rank', 'community_origin_democratic_republic_of_congo_rank', 'community_origin_denmark_rank', 'community_origin_dominica_rank', 
    'community_origin_dominican_republic_rank', 'community_origin_ecuador_rank', 'community_origin_egypt_rank', 'community_origin_el_salvador_rank', 'community_origin_eritrea_rank', 
    'community_origin_ethiopia_rank', 'community_origin_france_rank', 'community_origin_germany_rank', 'community_origin_ghana_rank', 'community_origin_greece_rank', 
    'community_origin_grenada_rank', 'community_origin_guatemala_rank', 'community_origin_guyana_rank', 'community_origin_haiti_rank', 'community_origin_honduras_rank', 
    'community_origin_hungary_rank', 'community_origin_india_rank', 'community_origin_indonesia_rank', 'community_origin_iran_rank', 'community_origin_iraq_rank', 
    'community_origin_ireland_rank', 'community_origin_israel_rank', 'community_origin_italy_rank', 'community_origin_jamaica_rank', 'community_origin_japan_rank', 
    'community_origin_jordan_rank', 'community_origin_kazakhstan_rank', 'community_origin_kenya_rank', 'community_origin_korea_rank', 'community_origin_kuwait_rank', 
    'community_origin_laos_rank', 'community_origin_latvia_rank', 'community_origin_lebanon_rank', 'community_origin_liberia_rank', 'community_origin_lithuania_rank', 
    'community_origin_malaysia_rank', 'community_origin_mexico_rank', 'community_origin_moldova_rank', 'community_origin_morocco_rank', 'community_origin_nepal_rank', 
    'community_origin_netherlands_rank', 'community_origin_nicaragua_rank', 'community_origin_nigeria_rank', 'community_origin_north_macedonia_rank', 'community_origin_norway_rank', 
    'community_origin_other_rank', 'community_origin_pakistan_rank', 'community_origin_panama_rank', 'community_origin_peru_rank', 'community_origin_philippines_rank', 
    'community_origin_poland_rank', 'community_origin_portugal_rank', 'community_origin_romania_rank', 'community_origin_russia_rank', 'community_origin_saudi_arabia_rank', 
    'community_origin_senegal_rank', 'community_origin_serbia_rank', 'community_origin_sierra_leone_rank', 'community_origin_singapore_rank', 'community_origin_somalia_rank', 
    'community_origin_south_africa_rank', 'community_origin_south_america_rank', 'community_origin_spain_rank', 'community_origin_sri_lanka_rank', 
    'community_origin_st_vincent_and_the_grenadines_rank', 'community_origin_sudan_rank', 'community_origin_sweden_rank', 'community_origin_switzerland_rank', 
    'community_origin_syria_rank', 'community_origin_thailand_rank', 'community_origin_total_rank', 'community_origin_trinidad_and_tobago_rank', 'community_origin_turkey_rank', 
    'community_origin_uganda_rank', 'community_origin_ukraine_rank', 'community_origin_united_kingdom_rank', 'community_origin_uruguay_rank', 'community_origin_uzbekistan_rank', 
    'community_origin_venezuela_rank', 'community_origin_vietnam_rank', 'community_origin_west_indies_rank', 'community_origin_yemen_rank', 'community_origin_zimbabwe_rank', 
    'environment_air_rank', 'environment_water_rank', 'environment_land_rank', 'environment_build_rank', 'vote_local_rank', 'vote_national_rank', 'tax_education_rank', 
    'tax_health_rank', 'tax_welfare_rank', 'housing_rent_median', 'housing_mortgage_median', 'community_language_percentage', 'community_origin_percentage', 
    'community_lgbt_percentage', 'diversity_cultural_index', 'diversity_economic_index', 'environment_air_index', 'environment_water_index', 'environment_land_index', 
    'environment_build_index', 'opportunity_population_count', 'opportunity_population_density', 'opportunity_employment_percentage', 'tax_education_percentage', 
    'tax_health_percentage', 'tax_welfare_percentage', 'vote_local_index', 'vote_national_index'
]

DATABASE_URL = "postgres://cwkqxbwhzlavuk:f26bde133b1aefe0221e588d71af31c2e3b6ecf685ea23c3a054e5df228b545d@ec2-3-212-143-188.compute-1.amazonaws.com:5432/db1mqjji0v9f85"


class RerootData:
    def __init__(self):
        self._conn = None
        self._curs = None
        self._parameters = None
        self._stats = None
        self._county_data = None
    

    def parameters(self):
        return self._parameters

    def stats(self):
        return self._stats

    def county_data(self):
        return self._county_data


    def create_conn(self):
        self._conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self._curs = self._conn.cursor()
    
    
    def close_conn(self):
        if self._curs:
            self._curs.close()
        if self._conn:
            self._conn.close()
    

    def query_data(self):
        self._curs.execute(PARAMETER_SQL)
        self._parameters = pd.DataFrame(self._curs.fetchall(), columns=PARAMETERS_HEADER)

        self._curs.execute(STATS_SQL)
        self._stats = pd.DataFrame(self._curs.fetchall(), columns=STATS_HEADER)

        self._curs.execute(COUNTY_DATA_SQL)
        self._county_data = pd.DataFrame(self._curs.fetchall(), columns=COUNTY_DATA_HEADER)
