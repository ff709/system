from pyhive import hive

conn = hive.Connection(host='node1',port=10000,username='hadoop')

cursor = conn.cursor()


def queryhives(sql,params,type='no_select'):
    params = tuple(params)
    cursor.execute(sql,params)
    if type != 'no_select':
        data_list = cursor.fetchall()
        conn.commit()
        return data_list
    else:
        conn.commit()
        return '数据库语句执行成功'

data = queryhives('select * from jobData',[],'select')[:1]
print(data)
