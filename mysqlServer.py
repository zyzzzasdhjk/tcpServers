import pymysql

# 连接数据库
conn = pymysql.connect(host='150.158.99.128'  # 连接名称，默认127.0.0.1
                       , user='root'  # 用户名
                       , passwd='5151'  # 密码
                       , port=3306  # 端口，默认为3306
                       , db='mms'  # 数据库名称
                       , charset='utf8'  # 字符编码
                       )
cur = conn.cursor()  # 生成游标对象
sql = "select * from `music` "  # SQL语句
cur.execute(sql)  # 执行SQL语句
data = cur.fetchall()  # 通过fetchall方法获得数据
for i in data[:2]:  # 打印输出前2条数据
    print(i)
cur.close()  # 关闭游标
conn.close()  # 关闭连接
