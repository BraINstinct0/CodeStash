###Format of sqlaccount.txt

#host=127.0.0.1
#port=80
#user=Username
#pass=passWORD
#db  =ICU_data_logs
#ENDED

#Place sqlaccount.txt in parent directory relative to this file. Otherwise, change file path string.

import pymysql
import os
import pandas as pd

def _get_account_data(filename):
    if not os.path.isfile(filename):
        raise FileNotFoundError()
    with open(filename, 'r') as f:
        lines=f.readlines()
        if (len(lines)==6)and((list(line[:5] for line in lines))==['host=','port=','user=','pass=','db  =', 'ENDED']):
            return (line[5:-1] for line in lines[:-1])
        else:
            raise SyntaxError()

def fetchsql(sql, chunksize=None):
    host, port, user, password, db=_get_account_data('../sqlaccount.txt')#edit this to path of sqlaccount.txt 
    connection=pymysql.connect(host=host,
                               port=int(port),
                               user=user,
                               password=password,
                               db=db,
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor
                              )
    try:
        with connection.cursor() as cursor:
            #cursor.execute(sql)
            #result=cursor.fetchone()
            #print(result)
            return pd.read_sql(sql, connection, chunksize=chunksize)
    finally:
        connection.close()
