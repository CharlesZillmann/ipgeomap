# This is a sample Python script.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import re
import geoip2.webservice
from dateutil.parser import *
from datetime import *
import sqlite3


##################################################################
# GLOBAL VARIABLES for IP Address Geographic Location
#
# https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en#accessing-geolite2-free-geolocation-data
# https://pypi.org/project/geoip2/
##################################################################
geoip_acctid = 721586
geoip_lickey = "dMQdxEjFqyu3FN0i"
# Cache Responses From rest Calls for Speed and Efficiency
ipgeocache = {str: [datetime.date, geoip2.models.City]}

##################################################################
# GLOBAL VARIABLES for Graphing
##################################################################
# Fixing random state for reproducibility
np.random.seed(19680801)


def dbinitialize ():
    con = sqlite3.connect('example.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE IF NOT EXISTS stocks
                   (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Create ipgeo table
    cur.execute('''CREATE TABLE IF NOT EXISTS ipgeo
                   (ipaddr text, 
                   date text, 
                   latitude text,
                   longitude text,
                   country_name text, 
                   country_iso_code text,
                   country_names text,
                   subd_ms_name text
                   subd_ms_iso_code text,
                   city_name text,
                   postal_code text,
                   traits_network text)''')

    # response.country.iso_code
    # response.country.name
    # response.country.names['zh-CN']
    # response.subdivisions.most_specific.name
    # response.subdivisions.most_specific.iso_code
    # response.city.name
    # response.postal.code
    # response.location.latitude
    # response.location.longitude
    # response.traits.network

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()


def dbverify ():
    con = sqlite3.connect('example.db')
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM stocks ORDER BY price'):
        print(row)


def dbuse ():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    cur.execute("create table lang (name, first_appeared)")

    # This is the qmark style:
    cur.execute("insert into lang values (?, ?)", ("C", 1972))

    # The qmark style used with executemany():
    lang_list = [
        ("Fortran", 1957),
        ("Python", 1991),
        ("Go", 2009),
    ]
    cur.executemany("insert into lang values (?, ?)", lang_list)

    # And this is the named style:
    cur.execute("select * from lang where first_appeared=:year", {"year": 1972})
    print(cur.fetchall())

    con.close()

def dbtest ():
    dbinitialize()
    dbverify()

##################################################################
# def ipaddrcontextdata
##################################################################
def ipaddrcontextdata (ipaddr):

    # This creates a Client object that can be reused across requests.
    # Replace "42" with your account ID and "license_key" with your license
    # key. Set the "host" keyword argument to "geolite.info" to use the
    # GeoLite2 web service instead of GeoIP2 Precision.

    with geoip2.webservice.Client(geoip_acctid, geoip_lickey, host="geolite.info") as client:
        # Replace "city" with the method corresponding to the web service
        # that you are using, i.e., "country", "city", or "insights". Please
        # note that Insights is not supported by the GeoLite2 web service.
        response = client.city(ipaddr)
        # print(type(response), ipaddr, ",",
        #       response.country.name, ",",
        #       response.city.name, ",",
        #       response.location.latitude, ",",
        #       response.location.longitude)
        # response.country.iso_code
        # response.country.name
        # response.country.names['zh-CN']
        # response.subdivisions.most_specific.name
        # response.subdivisions.most_specific.iso_code
        # response.city.name
        # response.postal.code
        # response.location.latitude
        # response.location.longitude
        # response.traits.network
    return response


##################################################################
# def parsefile_iplist
##################################################################
def parsefile_iplist ():
    datafile = "C:\\Users\\charl\\Documents\\SysLogFiles\\syslog_ssh.txt"
    default = date.today()

    patt = r"((([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[ (\[]?(\.|dot)[ )\]]?){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5]))"

    mycount = 0
    n_list = [int, str, [], str]
    ipaccumulated = []
    with open(datafile) as file:
        for line in file:
            iplisttemp = [match[0] for match in re.findall(patt, line)]
            ipaccumulated = ipaccumulated + iplisttemp
            date_1 = parse("Python is released in " + ' '.join(line.split()[0:2]), fuzzy=True, default=default)
            n_list.append([mycount, date_1, iplisttemp, line])
            print(n_list[len(n_list)-1])
            mycount = mycount + 1

    iplist = []
    [iplist.append(x) for x in ipaccumulated if x.replace("(", "").replace("[", "").replace(")", "").replace("]", "")
        .replace("dot", ".").replace(" ", "") not in iplist]

    for ipaddr in iplist:
        ipgeocache.update({ipaddr: [date.today(), ipaddrcontextdata(ipaddr)]})

    return iplist

##################################################################
# def random_walk
##################################################################
def random_walk(num_steps, max_step=0.05):
    """Return a 3D random walk as (num_steps, 3) array."""
    start_pos = np.random.random(3)
    steps = np.random.uniform(-max_step, max_step, size=(num_steps, 3))
    walk = start_pos + np.cumsum(steps, axis=0)
    return walk


##################################################################
# def update_lines
##################################################################
def update_lines(num, walks, lines):
    for line, walk in zip(lines, walks):
        # NOTE: there is no .set_data() for 3 dim data...
        line.set_data(walk[:num, :2].T)
        line.set_3d_properties(walk[:num, 2])
    return lines


dbtest()

# iplist = parsefile_iplist()
# print(iplist)
# print(ipgeocache)

# # Data: 40 random walks as (num_steps, 3) arrays
# num_steps = 30
# walks = [random_walk(num_steps) for index in range(len(iplist))]
#
# # Attaching 3D axis to the figure
# fig = plt.figure()
# ax = fig.add_subplot(projection="3d")
#
# # Create lines initially without data
# lines = [ax.plot([], [], [])[0] for _ in walks]
#
# # Setting the axes properties
# ax.set(xlim3d=(0, 1), xlabel='Time')
# ax.set(ylim3d=(0, 1), ylabel='Country')
# ax.set(zlim3d=(0, 1), zlabel='Count')
#
# # Creating the Animation object
# ani = animation.FuncAnimation(
#     fig, update_lines, num_steps, fargs=(walks, lines), interval=100)
#
# plt.show()