import requests
from fp.fp import FreeProxy
from ip2geotools.databases.noncommercial import DbIpCity
from timezonefinder import TimezoneFinder
import logging
import time
from webb import webb


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
    logging.debug(f"proxy:location:timezone:response code is  {proxy1}:{geo1}:{timez1}:{code} ")
    logging.debug(f"The RTT is {response.elapsed.total_seconds()} ")
    return response.status_code     # To print http response code   

def get_location(proxy):
    ip_address = proxy.split(":")[1][2:]
    geo = DbIpCity.get(ip_address, api_key='free')
    timezome = tf.timezone_at(lat=geo.latitude,lng=geo.longitude)
    return geo.city, timezome

def main():
    fp = FreeProxy(country_id=['US'])
    proxy1 = fp.get()
    #proxy2 = fp.get()
    #fp_list = fp.get_proxy_list(False)
    #print(f"length of list is {len(fp_list)}")
    geo1, timez1 = get_location(proxy1)
    print(proxy1)
    while False:
        code = request(proxy1)
        time.sleep(2)   

if __name__ == "__main__":
    main()

