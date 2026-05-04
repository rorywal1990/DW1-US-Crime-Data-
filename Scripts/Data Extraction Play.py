# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi

import requests
import json
import pandas as pd


response = requests.get(
    "https://api.usa.gov/crime/fbi/cde/agency/byStateAbbr/NY",
    params={"api_key": "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"}
    )

#print(response.text)

data = response.json()

rows = []
for county, agencies in data.items():
    for agency in agencies:
        agency["County"] = county
        rows.append(agency)
        
df = pd.DataFrame(rows)