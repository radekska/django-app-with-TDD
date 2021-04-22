import re
from collections import namedtuple

DB_DATA = namedtuple('db_data', ['user', 'password', 'name', 'host', 'port' ])

def parse_database_url(db_url):
    db_data = DB_DATA(
        user=re.search(r'\/\/(.+?):', db_url).group(1),
        password=re.search(r':(\w+)@', db_url).group(1),
        name=re.search(r'\/(\w+$)', db_url).group(1),
        host=re.search(r'@(.+):', db_url).group(1),
        port=int(re.search(r':(\d+)\/', db_url).group(1))
    )
    return db_data
    
    
    



