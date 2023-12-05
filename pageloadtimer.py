#!/usr/bin/env python
#
# Copyright (c) 2015 Corey Goldberg
# License: MIT
# this program will run test to 3 different sites and record the time it takes to load the page
# the time is recorded in a csv file
# the search keywords are predefined


import collections
import textwrap
import csv
import time
import webb
import os
import argparse
from selenium import webdriver
from datetime import datetime

import string
import random

parser = argparse.ArgumentParser()
parser.add_argument("--Fname", type=str, required=True,help="File Name")
FNAME = parser.parse_args().Fname

class PageLoadTimer:

    def __init__(self, driver):
        """
            takes:
                'driver': webdriver instance from selenium.
        """
        self.driver = driver

        self.jscript = textwrap.dedent("""
            var performance = window.performance || {};
            var timings = performance.timing || {};
            return timings;
            """)

    def inject_timing_js(self):
        timings = self.driver.execute_script(self.jscript)
        return timings

    def get_event_times(self):
        timings = self.inject_timing_js()
        # the W3C Navigation Timing spec guarantees a monotonic clock:
        #  "The difference between any two chronologically recorded timing
        #   attributes must never be negative. For all navigations, including
        #   subdocument navigations, the user agent must record the system
        #   clock at the beginning of the root document navigation and define
        #   subsequent timing attributes in terms of a monotonic clock
        #   measuring time elapsed from the beginning of the navigation."
        # However, some navigation events produce a value of 0 when unable to
        # retrieve a timestamp.  We filter those out here:
        good_values = [epoch for epoch in timings.values() if epoch != 0]
        # rather than time since epoch, we care about elapsed time since first
        # sample was reported until event time.  Since the dict we received was
        # inherently unordered, we order things here, according to W3C spec
        # fields.
        ordered_events = ('navigationStart', 'fetchStart', 'domainLookupStart',
                          'domainLookupEnd', 'connectStart', 'connectEnd',
                          'secureConnectionStart', 'requestStart',
                          'responseStart', 'responseEnd', 'domLoading',
                          )
        event_times = ((event, timings[event] - min(good_values)) for event
                       in ordered_events if event in timings)
        #print(f"secured start time is {timings['secureConnectionStart']}")
        return collections.OrderedDict(event_times)

def main():
    rows = []
    fields = ['dateTime', 'service site','searching string',\
              "navigationStart","fetchStart","domainLookupStart","domainLookupEnd",'connectStart','secureConnectionStart', \
              'connectEnd', 'requestStart','responseStart','responseEnd','domLoading']
    # these are the keywords we are going to search
    search_strings = ["Carnegie Mellon University", "Airbnb", "Facebook","Youtube","cirtic",\
                      "when would there be","search the map for new","suggestions on finals","start", \
                        "ending", "safety","data", "DDIO", "MSFG", "HOA", "FAFR", "WieSOichDichEmpfangen", "sagmichbitte", "ilAuraitSuffi"]
    counter = 0
    while counter < 3:
        time1 = time.time()
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        
        for search_string in search_strings:
            driver = webdriver.Firefox(options=options)

            url_google = "https://www.bing.com/search?q=" + search_string
            driver.get(url_google)
            timer = PageLoadTimer(driver)
            theTime = timer.get_event_times()
            # print(theTime)
            # print("\n")
            # if theTime['responseStart'] - theTime['requestStart'] - (theTime['secureConnectionStart'] - theTime['connectStart']) > 0:
            rows.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Bing", search_string, 
                            theTime['navigationStart'], theTime['fetchStart'],\
                            theTime['domainLookupStart'], theTime['domainLookupEnd'], \
                            theTime['connectStart'], theTime['secureConnectionStart'], \
                            theTime['connectEnd'], theTime['requestStart'], \
                            theTime['responseStart'], theTime['responseEnd'] , theTime['domLoading'] ])

            url_amazon = "https://www.amazon.com/s?k=" + search_string
            driver.get(url_amazon)
            timer = PageLoadTimer(driver)
            theTime = timer.get_event_times()
            if theTime['responseStart'] - theTime['requestStart'] - (theTime['secureConnectionStart'] - theTime['connectStart']) > 0:
                rows.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Amazon", search_string,\
                             theTime['navigationStart'], theTime['fetchStart'],\
                            theTime['domainLookupStart'], theTime['domainLookupEnd'], \
                            theTime['connectStart'], theTime['secureConnectionStart'], \
                            theTime['connectEnd'], theTime['requestStart'], \
                            theTime['responseStart'], theTime['responseEnd'] , theTime['domLoading'] ])

            url_X = "https://www.youtube.com/results?search_query=" + search_string
            driver.get(url_X)
            timer = PageLoadTimer(driver)
            theTime = timer.get_event_times()
            if theTime['responseStart'] - theTime['requestStart'] - (theTime['secureConnectionStart'] - theTime['connectStart']) > 0:
                rows.append([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Youtube", search_string,\
                             theTime['navigationStart'], theTime['fetchStart'],\
                            theTime['domainLookupStart'], theTime['domainLookupEnd'], \
                            theTime['connectStart'], theTime['secureConnectionStart'], \
                            theTime['connectEnd'], theTime['requestStart'], \
                            theTime['responseStart'], theTime['responseEnd'] , theTime['domLoading'] ])
            driver.quit()
        time2 = time.time()

        counter += 1
        print(f"Round {counter} finished with {time2 - time1} seconds")

    # name of csv file  
    filename = FNAME
        
    # writing to csv file  
    with open(filename, 'a') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 

if __name__ == '__main__':
    main()