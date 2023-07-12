from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析请求的URL
        parsed_url = urlparse(self.path)

        # 解析URL中的查询参数
        query_params = parse_qs(parsed_url.query)

        # 构造响应消息
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body>')
        self.wfile.write(b'<h1>Hello, World!</h1>')
        self.wfile.write(b'<p>Query Parameters:</p>')
        self.wfile.write(b'<ul>')
        for key, value in query_params.items():
            self.wfile.write(f'<li>{key}: {value[0]}</li>'.encode())
        self.wfile.write(b'</ul></body></html>')


if __name__ == '__main__':
    # 创建HTTP服务器并监听端口
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print(f'Starting server on port {server_address[1]}...')
    httpd.serve_forever()