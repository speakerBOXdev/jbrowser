import socket
import ssl
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100
class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack()
        self.scroll_y = 0
        self.scroll_x = 0
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<Left>", self.scrollleft)
        self.window.bind("<Right>", self.scrollright)
        
        self.window.bind("<Home>", self.scrolltop)
        self.window.bind("<End>", self.scrollbottom)
        self.window.bind("<MouseWheel>", self.scrollwheel)
        # self.window.bind("<Button-1>", self.scrollwheel)
        # self.window.bind("<Button-2>", self.scrollwheel)
        # self.window.bind("<Button-3>", self.scrollwheel)
        self.window.bind("<Button-4>", self.scrollwheel)
        self.window.bind("<Button-5>", self.scrollwheel)
        print("Hello, World!")

    def load(self, url):
        response=url.request()
        text=self.lex(response)
        self.display_list = layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        #print("scroll({},{})".format(self.scroll_x, self.scroll_y))
        for x, y, c in self.display_list:
            if y > self.scroll_y + HEIGHT: continue
            if y < VSTEP + self.scroll_y: continue
            if x > self.scroll_x + WIDTH: continue
            if x < HSTEP + self.scroll_x: continue
            self.canvas.create_text(x - self.scroll_x, y - self.scroll_y, text=c)

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

    def scrollwheel(self, e):       
        if e.num == 4:
            self.scrollup("")
        elif e.num == 5:
            self.scrolldown("")

    def scrolltop(self, e):
        self.scroll_x=0
        self.scroll_y=0
        self.draw()

    def scrollbottom(self, e):
        self.scroll_y=HEIGHT
        self.draw()

    def scrollleft(self, e):
        scroll=self.scroll_x-SCROLL_STEP
        if scroll < 0:
            scroll=0
            
        if scroll != self.scroll_x:
            self.scroll_x=scroll
            self.draw()

    def scrollright(self, e):
        scroll=self.scroll_x+SCROLL_STEP
        if scroll > WIDTH:
            scroll=WIDTH
            
        if scroll != self.scroll_x:
            self.scroll_x=scroll
            self.draw()

    def scrolldown(self, e):
        scroll=self.scroll_y+SCROLL_STEP
        if scroll > HEIGHT:
            scroll=HEIGHT
        
        if scroll != self.scroll_y:
            self.scroll_y=scroll
            self.draw()

    def scrollup(self, e):
        scroll=self.scroll_y-SCROLL_STEP
        if self.scroll_y-SCROLL_STEP < 0:
            scroll=0
        
        if scroll != self.scroll_y:
            self.scroll_y=scroll
            self.draw()

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

def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        if c == "\n":
            cursor_y+=VSTEP
            cursor_x=HSTEP
        else:            
            display_list.append((cursor_x, cursor_y, c))
            cursor_x+=HSTEP

        # if (cursor_x >= WIDTH-HSTEP):
        #     cursor_x=HSTEP
        #     cursor_y+=VSTEP   

    return display_list

def get_entity_val(entity):
    if entity == "&lt;":
        return "<"
    elif entity == "&gt;":
        return ">"
    return ""

if __name__ == "__main__":
    import sys
    url=sys.argv[1]
    Browser().load(URL(url))
    tkinter.mainloop()
