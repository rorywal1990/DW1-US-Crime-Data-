# -*- coding: utf-8 -*-
"""
Created on Tue May  5 18:53:17 2026

@author: roryw
"""

import requests
import pandas as pd
import us
import time


def get_states():
    
    """
    Generate a list of all 50 US state codes
    
    :returns: A list of all 50 US state codes
    
    >>> states = get_states()
    
    """
    
    return [state.abbr for state in us.states.STATES]





def get_url():
    
    """
    Get the URL for the US crime data webpage we are pulling everything from
    
    :returns: the URL
    
    >>> url = get_url()
    
    """
    
    return "https://api.usa.gov/crime/fbi/cde/"





def get_agency_ext():
    
    """
    Get the extension for the Agency data. This will be appended to the URL so we can make a 
    call to the Agency data to extract it. The state name has been deliberately excluded so we
    can pull all on a loop
    
    :returns: the extension for the Agency URL
    
    >>> ext = get_agency_ext()
    api_url = url + ext + state
    
    """
    
    return "agency/byStateAbbr/"





def api_call(url, ext, ext_ok):
    
    """
    Make the call to the API & return the results as a dataframe
    
    :param url: the url for the US Crime database
    :param ext: the extension for the URL, defining which data we want to pull 
    :param ext_ok: returns 1 if the extraction has been successful and 0 if not
    :returns: the relevant data as a dataframe. If extraction fails then an error variable is returned
    
    >>> df = api_call(url = "https://api.usa.gov/crime/fbi/cde/", ext = "agency/byStateAbbr/")
    
    """
    
    ext_ok = 0
    retries = 0
    df = pd.DataFrame(None)
    
    while retries < 5:
    
        response = requests.get(
            url + ext,
            params = {"api_key": "iiHnOKfno2Mgkt5AynpvPpUQTEyxE77jo1RU8PIv"}
            )
        
        if response.status_code != 200:
            retries += 1
            print("Extraction error. Attempting retry: ", retries)
            time.sleep(5)
            
        else:
            print("Successful extraction")
            ext_ok = 1
            retries = 5
            df = api_to_df(response.json())
    
    return df, ext_ok


 
    

def api_to_df(api_call):
    
    """
    Turn an API call into a dataframe.
    
    :params api_call: an API call (requests.get) converted to json
    :returns: the API call as a dataframe
    
    >>> response = requests.get(http, params = {})
        api_call = response.json()
        df = api_to_df(api_call)
    
    """
    
    rows = []
    for values in api_call.values():
        for value in values:
            rows.append(value)
            
    data = pd.DataFrame(rows)
            
    return data




def get_agency_data():
    
    """
    Get the agency data as a dataframe by making an API call & converting it. The model will attempt to
    pull data for each state. If it fails, it will wait 5s and retry, up to a maximum of 5 times. If 
    extraction for that state is successful then the state is removed from the list. Once the full list
    has been cycled through then any remaining states will be retried as before, with the overall process
    repeating either until all states have been pulled or 5 full retries have been attempted.
    
    :returns: Agency data as a dataframe & the list of any states that did not get data pulled for them
    
    >>>agency_data = get_agency_data

    """    
    
    full_data = pd.DataFrame(None)
    states = get_states()
    states.remove("VA") # Virginia missing from dataset    
    
    #Kill the loop either if we have an error with one of the states or if all states are pulled
    extraction_ok = 1
    all_states = 0
    retries = 0
    
    while all_states == 0 and retries < 5:
        
        #Get the last state in the list. Each time we will use this to see if we have reached the end
        #of the list yet, which is a trigger for retrying or ending the loop
        last_state = states[len(states)-1]
        
        for state in states:
            print("Attempting extraction for ", state)
            state_data, extraction_ok = api_call(url = get_url(), ext = get_agency_ext() + state, ext_ok = extraction_ok)
        
            #If extraction is successful then store the data and remove the state from the list so
            #we don't try to pull it again.
            if extraction_ok == 1:
                full_data = pd.concat([full_data, state_data], axis = 0)
                states.remove(state)
                print(str(len(states)) + " States Remaining")
                
            #Check if we have ran out of states (because they are all in) or if we need to have another pass
            #because some were missed
            if len(states) == 0:
                all_states = 1
                extraction_ok = 1
            
            elif state == last_state:
                retries += 1
                

    return full_data, states

