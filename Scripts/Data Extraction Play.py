# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#https://cde.ucr.cjis.gov/LATEST/webapp/#/pages/docApi

import importlib
import us_crime_functions as usc

importlib.reload(usc)




try:

    raw_data, extraction_ok, failed_states = usc.get_agency_data()
    
    #Write extracted data to database
    
    if len(failed_states) == 0:
        print("Missing States")
        #Write failed states to database
        #Build out something later that looks as that list of failed states & tries again.
        #Overwrite list each time so we don't retry something we have successfully pulled.
    
    
except:
    print("There has been an error")


#Testing & error checks




