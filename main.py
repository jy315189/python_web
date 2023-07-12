import datetime
import pymysql
import web
import tsjx_fun
urls = (
    '/', 'index',
    '/process', 'process'
)
sqlData = ''  # 定义全局变量


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
