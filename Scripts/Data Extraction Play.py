# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi

import us_crime_functions as usc


try:

    raw_data, extraction_ok = usc.get_agency_data()
    
    if extraction_ok == 1:
        print("Success")
    else:
        print("Fail")
    
    
except:
    print("There has been an error")


#Testing & error checks




