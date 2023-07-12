import web

urls = (
    '/', 'index',
)


class index:
    def GET(self):
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()


if __name__ == "__main__":
    app = web.application(urls, globals())
    server = app.wsgifunc()
    web.httpserver.runsimple(server, ('192.168.1.115', 8888))
