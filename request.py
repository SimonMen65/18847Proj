import requests
from fp.fp import FreeProxy
from ip2geotools.databases.noncommercial import DbIpCity
from timezonefinder import TimezoneFinder
import logging
import time

tf = TimezoneFinder() 
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
 
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def request(p):
    session = requests.Session()
    session.proxies = p

    url = 'https://geonode.com/free-proxy-list'
    response = session.get(url)       # To execute get request 
    return response.status_code     # To print http response code   

def get_location(proxy):
    ip_address = proxy.split(":")[1][2:]
    geo = DbIpCity.get(ip_address, api_key='free')
    timezome = tf.timezone_at(lat=geo.latitude,lng=geo.longitude)
    return geo.city, timezome

if __name__ == "__main__":
    #fp = FreeProxy(rand=True,country_id=['US'])
    fp = FreeProxy(country_id=['US'])
    proxy1 = fp.get()
    #proxy2 = fp.get()
    #fp_list = fp.get_proxy_list(False)
    #print(f"length of list is {len(fp_list)}")
    geo1, timez1 = get_location(proxy1)
    print(proxy1)
    while True:
        code = request(proxy1)
        logging.debug(f"proxy is {proxy1} location is {geo1} timezone is {timez1} response code is {code} ")
        time.sleep(2)

