# 导入所需的模块
from http import server
import http
from http.server import BaseHTTPRequestHandler, HTTPServer, HTTPStatus
import os
import urllib
import json
import requests
import ssl
import re

# 定义小红书服务器的URL，请根据实际情况修改。
xhs_server = "http://127.0.0.1/xhs/"

# 编译一个正则表达式模式，用于匹配URL
regular = re.compile("http[s]?://[a-zA-Z0-9./?=&_]+")

# 创建一个自定义的请求处理类，继承自BaseHTTPRequestHandler
class Resquest(BaseHTTPRequestHandler):
    # 处理GET请求的方法
    def do_GET(self):
        # 打印请求的路径
        print(self.path)
        # 如果路径是根目录（'/'），则发送200响应，并读取并发送HTML文件
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            with open("download_head.html", 'r', encoding='utf-8') as fh, open("download_foot.html", 'r', encoding='utf-8') as ff:
                content_head = fh.read()
                content_foot = ff.read()
                self.wfile.write(content_head.encode() + content_foot.encode())
        else:
            # 尝试打开请求的文件路径
            try:
                path = urllib.parse.unquote(self.path[1:])
                with open(path, 'rb') as f:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                # 如果文件不存在，则发送404响应
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'<h1>File Not Found</h1>')

    # 处理POST请求的方法
    def do_POST(self):
        try:
            # 获取POST请求的内容长度，并读取请求体中的数据
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            post_data = json.loads(post_data)
            print(type(post_data), post_data)
            # 获取URL参数
            url = post_data.get('url', '')
            if url:
                print(url)
            else:
                # 如果缺少必要的参数，则返回错误信息
                html_text = """<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: center; height: 100vh;">
                <p> 解析错误，缺少必要的参数</p>
                </div>
                """
                self.return_html(html_text, 422)
                print('缺少必要的参数')
                return
            # 使用正则表达式查找所有匹配的URL
            url_list = re.findall(regular, url)
            print('video_url_list ===>', url_list)
            for o_url in url_list:
                print('video_url ===>', o_url)
                data = {
                    "url": o_url
                }
                # 向小红书服务器发送POST请求
                responses = requests.post(xhs_server, json=data)
                data = responses.json()
                print(responses.status_code, 'code================', data)
                # 获取下载地址和动图地址的数量
                print(len(data['data'].get('下载地址')))
                print(len(data['data'].get('动图地址')))
                if responses.status_code != 200:
                    raise Exception(data)
                if responses.status_code == 200:
                    # 获取下载地址、动图地址、作者昵称和作品描述
                    download_url = data['data'].get('下载地址')
                    liveimg_url = data['data'].get('动图地址')
                    user_name = data['data'].get('作者昵称')
                    desc_content = data['data'].get('作品描述')
                    # 构建HTML文本，包含下载按钮和视频/图片播放器
                    html_text = f"""<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: center; height: 100vh;">
                    <a id="user_name" style="display: none;">{user_name}</a>
                    <a id="desc_content" style="display: none;">{desc_content}</a>
                    <div style="display: flex; flex-direction: column; align-items: center; flex-basis: 100%;">
                      <button onclick="copyToClipboard('user_name')">点击复制作者名称</button>
                      <p></p>
                      <button onclick="copyToClipboard('desc_content')">点击复制作品文案</button>
                    </div>
                    """
                    for i in range(len(download_url)):
                        if liveimg_url[i]:
                            d_url = liveimg_url[i]
                        else:
                            d_url = download_url[i]
                        d_url = re.sub(r'http:', 'https:', d_url)
                        # 根据文件类型构建不同的HTML元素
                        if re.search('format/png', d_url):
                            fileName = d_url.split('?')[0]
                            fileName = fileName.split('/')[-1] + '.png'
                            html_text += f""" 
                            <div style="display: flex; flex-direction: column; align-items: center; flex-basis: 100%;">
                                <img src={d_url} style="max-height: calc(100vh / 3); width: auto; height: auto; object-fit: contain;">
                                </img>
                                <button class="download-button" style="margin-top: 10px;" onclick="downloadFile('{d_url}', '{fileName}')">下载图片</button>
                            </div>
                            """
                        elif re.search('/pre_post', d_url):
                            fileName = d_url.split('/')[-1] + '.mp4'
                            html_text += f""" 
                            <div style="display: flex; flex-direction: column; align-items: center; flex-basis: 100%;">
                                <video controls src="{d_url}" style="max-height: calc(100vh / 3); width: auto; height: auto; object-fit: contain;" type="video/mp4" poster>
                                    您的浏览器不支持 video 标签。
                                </video>
                                <button class="download-button" style="margin-top: 10px;" onclick="downloadFile('{d_url}', '{fileName}')">下载视频</button>
                            </div>
                            """
                        else:
                            fileName = d_url.split('/')[-1]
                            html_text += f"""
                            <div style="display: flex; flex-direction: column; align-items: center; flex-basis: 100%;">
                                <video controls src="{d_url}" style="max-height: calc(100vh / 3); width: auto; height: auto; object-fit: contain;" type="video/mp4" poster>
                                    您的浏览器不支持 video 标签。
                                </video>
                                <button class="download-button" style="margin-top: 10px;" onclick="downloadFile('{d_url}', '{fileName}')">下载视频</button>
                            </div>
                            """
                    html_text += "</div>"
                self.return_html(html_text, 200)
        except Exception as err:
            # 如果发生异常，则返回错误信息
            html_text = f"""<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: center; height: 100vh;">
                <p> 解析错误，{err}</p>
                </div>
                """
            print(err)
            self.return_html(html_text, 422)

    # 解析查询字符串的方法
    def parse_query(self):
        self.queryString = urllib.parse.unquote(self.path.split('?', 1)[1])
        self.queries = urllib.parse.parse_qs(self.queryString)
        print(self.queries)

    # 返回HTML响应的方法
    def return_html(self, html_text, status_code):
        with open("download_head.html", 'r', encoding='utf-8') as fh, open("download_foot.html", 'r', encoding='utf-8') as ff:
            content_head = fh.read()
            content_foot = ff.read()
        if not html_text:
            html_text = "解析错误"
        html_text = content_head.encode() + html_text.encode() + content_foot.encode()
        # 发送响应状态码
        self.send_response(status_code)
        # 添加CORS头
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(html_text))
        self.end_headers()
        self.wfile.write(html_text)

# 主函数
if __name__ == '__main__':
    # 设置服务器监听的主机和端口
    host = ('0.0.0.0', 8888)
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)

    # 创建SSL上下文
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # 使用SSL上下文包装socket
    server.socket = context.wrap_socket(server.socket, server_side=True)

    # 启动服务器
    server.serve_forever()