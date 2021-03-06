# -*- coding: utf-8 -*-
"""REASAS.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qMAp_8OZIEPwbeIVj1H_1vvmneeO8ZL7
"""

import requests
import json
import pandas as pd
from pandas import json_normalize

url = "https://opendata.resas-portal.go.jp"

#個人で取得したAPIKEYを入力↓
headers = {
    "X-API-KEY":"xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
#都道府県一覧→都道府県コード・都道府県名
r = requests.get(url+"/api/v1/prefectures", headers = headers).json()

#都道府県一覧
def prefectures():
    code = "/api/v1/prefectures"
    r = requests.get(url+code, headers = headers).json()
    df_prefectures = json_normalize(r["result"])
    return df_prefectures

#市区町村一覧
def cities(pref_code):
    code = "/api/v1/cities"
    payload ={"prefCode": pref_code}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_cities = json_normalize(r["result"])
    return df_cities

#産業大分類
def industries_broad():
    code ="/api/v1/industries/broad"
    r = requests.get(url+code, headers = headers).json()
    df_industries_broad = json_normalize(r["result"])
    return df_industries_broad

#産業中分類
def industries_middle():
    code ="/api/v1/industries/middle"
    r = requests.get(url+code, headers = headers).json()
    df_industries_middle = json_normalize(r["result"])
    return df_industries_middle

#産業小分類
def industries_narrow():
    code ="/api/v1/industries/narrow"
    r = requests.get(url+code, headers = headers).json()
    df_industries_narrow = json_normalize(r["result"])
    return df_industries_narrow

#職業大分類
def jobs_broad():
    code ="/api/v1/jobs/broad"
    r = requests.get(url+code, headers = headers).json()
    df_jobs_broad = json_normalize(r["result"])
    return df_jobs_broad

#職業中分類→中分類コードが絞れない
def jobs_middle(jobs_code):
    code ="/api/v1/jobs/middle"
    payload = {"iscoCode":jobs_code}
    r = requests.get(url+code, headers = headers, payload = params).json()
    df_jobs_middle = json_normalize(r["result"])
    return df_jobs_middle

#人口構成 prefCode:都道府県コード, cityCode:市区町村コード(すべての市区町村は-を送る)
#0：総人口　1：年少人口　2：生産年齢人口　3：老年人口
def population_composition_perYear(prefCode, cityCode, species):
    code = "/api/v1/population/composition/perYear"
    payload = {"prefCode":prefCode, "cityCode":cityCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_population_composition_perYear = json_normalize(r["result"]["data"][species]["data"])
    return df_population_composition_perYear

#人口ピラミッド
#0-14（年少人口）, 15-64（生産年齢人口）, 65-（老年人口）✕人数・割合
def population_composition_pyramid(prefCode, cityCode, yearLeft, yearRight):
    code = "/api/v1/population/composition/pyramid"
    payload = {"prefCode":prefCode, "cityCode":cityCode, "yearLeft":yearLeft, "yearRight":yearRight}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_population_composition_pyramid_left = json_normalize(r["result"]["yearLeft"]["data"])
    df_population_composition_pyramid_right = json_normalize(r["result"]["yearRight"]["data"])
    return {"yearleft":df_population_composition_pyramid_left, "yearright":df_population_composition_pyramid_right}

#人口増減率
def population_sum_perYear(prefCode, cityCode):
    code = "/api/v1/population/sum/perYear"
    payload = {"prefCode":prefCode, "cityCode":cityCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_population_composition_sum_perYear = json_normalize(r["result"]["bar"]["data"]).drop("class", axis=1)
    return df_population_composition_sum_perYear

#出生数・死亡数/転入数・転出数
#総人口：soujinkou, ttss：出生数・死亡数・転入率・転出数
def population_sum_estimate(prefCode,cityCode):
    code = "/api/v1/population/sum/estimate"
    payload = {"prefCode":prefCode, "cityCode":cityCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    soujinkou = json_normalize(r["result"]["data"][0]["data"])
    soujinkou =soujinkou.rename(columns = {"value":"soujinkou"})
    tennyu = json_normalize(r["result"]["data"][1]["data"])
    tennyu = tennyu.rename(columns = {"value":"tennyu"})
    tensyutu =  json_normalize(r["result"]["data"][2]["data"])
    tensyutu  = tensyutu.rename(columns = {"value":"tensyutu"})
    syussei =  json_normalize(r["result"]["data"][3]["data"])
    syussei  = syussei.rename(columns = {"value":"syussei"})
    sibou =  json_normalize(r["result"]["data"][4]["data"])
    sibou = sibou.rename(columns = {"value":"sibou"})
    ttss = pd.concat([tennyu,tensyutu["tensyutu"],syussei["syussei"],sibou["sibou"]], axis=1)
    # ttss = ttss.rename(columns = {"value":"tennyu","value":"tensyutu","value":"syussei","value":"sibou"})
    return {"soujinkou":soujinkou, "ttss":ttss}

#新卒者就活・進学→反応なし
#prefecture_code
#display/Method(0:実数, 1:就職率・進学率)
#matter(0：地元就職, 1：流出, 2：流入, 3：純流入)
#classification(0:就職・進学の合計, 1:進学, 2:就職)
#display/type(00:すべての就職・進学, 10:すべての進学, 11:大学進学, 12:短期大学進学, 20:就職)
#gender(0:総数, 1:男性, 2:女性)
def EAT(prefecture_cd, displayMethod, matter, classification, displayType, gender):
    code = "/api/v1/employEducation/localjobAcademic/toTransition"
    payload = {"prefecture_cd":prefecture_cd,"displayMethod":displayMethod, "matter":matter,"classification":classification, "displayType":displayType, "gender":gender}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_eat = json_normalize(r["result"]["changes"][0]["data"])
    return df_eat

#将来人口推計 year:指定可能年度2040, prefcode: 都道府県コード
def population_future(year, prefCode):
    code = "/api/v1/population/future/cities"
    payload = {"year": year, "prefCode": prefCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_population_future = json_normalize(r["result"]["cities"])
    return df_population_future

#産業別特化係数 year: 指定可能年度2012年
def power_forlndustry(year,prefCode,cityCode,sicCode):
    code = "/api/v1/industry/power/forIndustry"
    payload = {"year":year, "prefCode":prefCode, "cityCode":cityCode, "sicCode":sicCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_power_forlndustry = json_normalize(r["result"]["data"])
    return df_power_forlndustry

#地域別特化係数
def power_forArea(year, prefCode, areaType, dispType, sicCode, simcCode):
    code = "/api/v1/industry/power/forArea"
    payload = {"year":year, "prefCode":prefCode, "areaType":areaType, "dispType":dispType, "sicCode":sicCode, "simcCode":simcCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_power_forArea = json_normalize(r["result"]["prefectures"])
    return df_power_forArea

#製造業事業所単位分析_継続・参入・退出事業所別の推移
def power_forManufacturerEstablishments(prefCode, sicCode, simcCode):
    code = "/api/v1/industry/power/forManufacturerEstablishments"
    payload = {"prefCode":prefCode, "sicCode":sicCode, "simcCode":simcCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_taishutu = json_normalize(r["result"]["establishments"][0]["data"])
    df_zenjigyousyo = json_normalize(r["result"]["establishments"][1]["data"])
    df_sannyu =  json_normalize(r["result"]["establishments"][2]["data"])
    df_forManufacturerEstablishments = {"df_taishutu":df_taishutu, "df_zenjigyousyo":df_zenjigyousyo, "df_sannyu":df_sannyu}
    return df_forManufacturerEstablishments

#企業数
def municipality_company_perYear(prefCode, cityCode, sicCode, simcCode):
    code = "/api/v1/municipality/company/perYear"
    payload = {"prefCode":prefCode, "cityCode":cityCode, "sicCode":sicCode, "simcCode":simcCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_municipality_company_perYear = json_normalize(r["result"]["data"])
    return df_municipality_company_perYear


#観光・宿泊系
#居住都道府県別の延べ宿泊者数（日本人）の推移
def guest_prefLine(year, prefCode, cityCode, addOppPrefCode):
    code = "/api/v1/tourism/guest/prefLine"
    payload = {"year":year, "prefCode":prefCode, "cityCode":cityCode, "addOppPrefCode":addOppPrefCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_guest_prefLine = json_normalize(r["result"]["changes"][0]["data"])
    return df_guest_prefLine

#宿泊施設数の推移
#保留
def hotelAnalysis_facilityStack(display, unit, prefCode):
    code = "/api/v1/tourism/hotelAnalysis/facilityStack"
    payload = {"display":display, "unit":unit, "prefCode":prefCode}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_hotelAnalysis_facilityStack = json_normalize(r["result"]["data"][0]["years"])
    return df_hotelAnalysis_facilityStack

#一人あたり賃金
def wages_perYear(prefCode, sicCode, simcCode, wagesAge):
    code = "/api/v1/municipality/wages/perYear"
    payload = {"prefCode":prefCode, "sicCode":sicCode, "simcCode":simcCode, "wagesAge":wagesAge}
    r = requests.get(url+code, headers = headers, params = payload).json()
    df_wages_perYear = json_normalize(r["result"]["data"])
    df_wages_perYear = df_wages_perYear.rename(columns= {"value":"一人あたり賃金"})
    print(r["result"]["prefName"])
    return df_wages_perYear

wages_perYear(13, "-", "-", 4)

hotelAnalysis_facilityStack(2,0,1)

guest_prefLine(2015, 1, "-", 12)

municipality_company_perYear(11, "-", "E", "20")

tmp = power_forManufacturerEstablishments(11, "E", 20)
tmp["df_zenjigyousyo"]

power_forArea(2012, 11, 1, 1, "E", 20)

power_forlndustry(2012, 1, "-", "-")

population_future(2040, 1)

EAT(1, 0, 1, 1, 10, 0)

tmp = population_sum_estimate(1,"-")
tmp["soujinkou"]

tmp = population_composition_pyramid(1,"-",1980,2015)
tmp["yearright"]



df_population_composition

df_sikutyouson

