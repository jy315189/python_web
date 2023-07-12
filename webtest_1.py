import datetime
import pymysql
import web
import tsjx_fun
urls = (
    '/', 'index',
    '/process', 'process'
)
sqlData = ''  # 定义全局变量


# def generate_sqls(data):
#     # 将字符串拆分成列表
#     data_list = data.split(',')
#     first_23 = data_list[:23]
#
#     listName = ["硝酸配置槽液位", "硝酸萃取配料计量槽液位", "硝酸高位槽液位", "溶解反应槽液位", "气体探测器1",
#                 "气体探测器2", "气体探测器3", "气体探测器4", "气体探测器5", "气体探测器6", "气体探测器7",
#                 "气体探测器8", "气体探测器9", "1号罐体液位", "2号罐体液位", "3号罐体液位", "4号罐体液位",
#                 "5号罐体液位", "6号罐体液位", "7号罐体液位", "8号罐体液位", "9号罐体液位", "10号罐体液位"]
#
#     # 生成sql1列表
#     sql1_list = []
#     for i in range(len(first_23)):
#         sql1 = "insert into collectdata_copy1 (NAME,QUALITY,TIME,VALUE) values ('" + listName[
#             i] + "','GOOD','" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "','" + first_23[i] + "')"
#         sql1_list.append(sql1)
#
#     # 生成sql2
#     sql2 = "INSERT INTO `bxasafety_whp`.`whp_lrlydj` (`id`, `lydw`, `create_date`, `lrr`) VALUES ('{}', '{}', '{}', '{}')".format(
#         data_list[23], data_list[24], data_list[25], data_list[26])
#     sql1_list.append(sql2)
#
#     # 生成sql3
#     sql3 = "INSERT INTO `bxasafety_whp`.`whp_lrlydj_info` (`id`, `lrlydj_id`, `whp_id`, `sfsl`, `jcl`, `sync_timestamp`,`jbr`) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')".format(
#         data_list[27], data_list[28], data_list[29], float(data_list[30]), data_list[31], data_list[32], data_list[32])
#     sql1_list.append(sql3)
#
#     # 返回简单的列表
#     return sql1_list

# def insert_sql(data):
#     sql_list = data
#
#     # 连接到数据库
#     conn = pymysql.connect(host="127.0.0.1", user="zhjx", passwd="123456", db="zhdp_whp", charset='utf8mb4')
#
#     # 创建游标对象
#     cursor = conn.cursor()
#
#     # 循环执行SQL语句
#     for sql in sql_list:
#         try:
#             cursor.execute(sql)
#         except pymysql.Error as err:
#             print(err)
#
#     # 提交事务
#     conn.commit()
#     # 关闭游标和数据库连接
#     cursor.close()
#     conn.close()




class index:
    def GET(self):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()


class process:
    def POST(self):
        data = web.input()  # 获取前端发送的数据
        message1 = data.get('message1')  # 获取 message1 字段的值
        # 在这里进行对 message1 数据的处理
        sqlData = message1  # 将 message1 赋值给全局变量 sqlData
        # 在这里进行对 sqlData 数据的处理
        # ...
        insert_data = tsjx_fun.generate_sqls(sqlData)
        print(insert_data)
        result = tsjx_fun.insert_sql(insert_data)  # 假设处理结果为 True
        print(result)
        return str(result)  # 将处理结果转换成字符串并返回


if __name__ == "__main__":
    from cheroot.server import HTTPServer
    from cheroot.ssl.builtin import BuiltinSSLAdapter

    HTTPServer.ssl_adapter = BuiltinSSLAdapter(
        certificate='cert/server.crt',
        private_key='cert/server.key')
    app = web.application(urls, globals())
    server = app.wsgifunc()

    web.httpserver.runsimple(server, ('192.168.1.115', 8888))
