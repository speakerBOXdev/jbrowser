import socket
import ssl
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()

    def load(self, url):
        
        response=url.request()
        text=self.lex(response)
        cursor_x, cursor_y = HSTEP, VSTEP
        for c in text:
            if c == "\n":
                cursor_y+=VSTEP
                cursor_x=HSTEP
            else:
                self.canvas.create_text(cursor_x, cursor_y, text=c)
            cursor_x+=HSTEP
            if (cursor_x >= WIDTH-HSTEP):
                cursor_x=HSTEP
                cursor_y+=VSTEP

    def lex(self, body):
        text = ""
        in_tag = False
        in_entity = False
        entity=""
        
        for c in body:
            if c == "<":
                in_tag = True
            elif c == ">":
                in_tag = False
            elif c == "&":
                in_entity = True
                entity="&"
            elif c == ";":
                in_entity = False
                entity=entity+";"
                entityValue=get_entity_val(entity)
                text+=entityValue
                entity=""
            elif not in_tag:
                if in_entity:
                    entity+=c
                else:
                    text+=c
        return text

class URL:
    def __init__(self, url=""):
        if (url == ""):
            url="file:///home/josh/jbrowser/tests/resources/simple.html"

        self.scheme, url = url.split("://", 1)
        assert self.scheme in ["http", "https", "file", "data"]
        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443
        elif self.scheme == "data":
            content_type, content=url.split(",", 1)
            if (content_type == "/text/html"):
                self.content=content

        if "/" not in url:
            url = url + "/"
        self.host, url = url.split("/", 1)
        self.path = "/" + url
    
        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

    def add_header(self, request, header, value):
        request += "{}: {}\r\n".format(header, value)
        return request

    def request(self):

        if self.scheme == "file":
             with open(self.path, 'r') as file:
                content=file.read()
             return content
        elif self.scheme == "data":
            content=self.content
            return content
           
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP
        )

        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        s.connect((self.host, self.port))

        request = "GET {} HTTP/1.0\r\n".format(self.path)
        request = self.add_header(request, "Host", self.host)
        request = self.add_header(request, "Connection", "close")
        request = self.add_header(request, "User-Agent", "jbrowser-0.1")
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf-8", newline="\r\n")

        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()

        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers

        content = response.read()
        s.close()

        return content

def get_entity_val(entity):
    if entity == "&lt;":
        return "<"
    elif entity == "&gt;":
        return ">"
    return ""

def load(url):
    body = url.request()
    show(body)


if __name__ == "__main__":
    import sys
    url=sys.argv[1]
    Browser().load(URL(url))
    tkinter.mainloop()
