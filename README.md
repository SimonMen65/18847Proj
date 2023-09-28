# 18847Proj

## SetUp
Create a python virtual env or Conda Env for this project:

`conda create --name 18847` \
`pip3 install requests` \

A public package can help up fetch freeproxy lists and configure proxy automatically:\
`pip3 install free-proxy`
But they only have 1 or 2 working proxies in US

However, this cannot give exact location info, so we need another package
`pip3 install ip2geotools`\
But this request is quite slow, it could take seconds.
So I suggest we set up a local HashMap to check if the ip has been logged before

To acquire the time zone, we need package
`pip3 install timezonefinder`

