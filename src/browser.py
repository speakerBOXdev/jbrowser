import socket
import ssl
import tkinter

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 12, 18
SCROLL_STEP = 100
class Browser:
    def __init__(self):

        self.width=WIDTH
        self.height=HEIGHT

        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill="both",expand=True)
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
        self.window.bind("<Configure>", self.configure)
        

    def load(self, url):
        response=url.request()
        text=self.lex(response)
        self.display_list = layout(text)

        self.max_x=0
        self.max_y=0
        for x, y, c in self.display_list:
            if x > self.max_x: self.max_x=x
            if y > self.max_y: self.max_y=y

        self.draw()

    def draw(self):
        self.canvas.delete("all")

        scroll_x_visible=self.max_x > self.width
        scroll_y_visible=self.max_y > self.height

        for x, y, c in self.display_list:
            if y > self.scroll_y + self.height: continue
            if y < VSTEP + self.scroll_y: continue
            if x > self.scroll_x + self.width: continue
            if x < HSTEP + self.scroll_x: continue
            self.canvas.create_text(x - self.scroll_x, y - self.scroll_y, text=c)

        scrollbar_color="#229"
        scrollbar_thickness=5
        scrollbar_window_offset=2 # scrollbar window padding
        scrollbar_offset=15 # scrollbar offset at ends
        if scroll_y_visible == True:
            x0=self.width-scrollbar_thickness-scrollbar_window_offset
            x1=self.width-scrollbar_window_offset

            y0=self.scroll_y+scrollbar_window_offset+scrollbar_offset
            viewport_percentage=self.height/self.max_y            
            y1=self.scroll_y+(self.height-scrollbar_window_offset-scrollbar_offset)*viewport_percentage

            self.canvas.create_rectangle(x0, y0, x1, y1, fill=scrollbar_color)
        if scroll_x_visible == True:

            x0=self.scroll_x+scrollbar_offset
            viewport_percentage=self.width/self.max_x
            x1=self.scroll_x+(self.width-scrollbar_window_offset-scrollbar_offset)*viewport_percentage
            y0=self.height-scrollbar_thickness-scrollbar_window_offset
            y1=self.height-scrollbar_window_offset
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=scrollbar_color)

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

    def configure(self, e):
        if self.width != e.width or self.height != e.height:
            #print("Configure - previous:{}x{}; current:{}x{}".format(self.width, self.height, e.width, e.height))
            self.width=e.width
            self.height=e.height
            #self.canvas.pack()
            self.draw()
        

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
        self.scroll_y=self.height
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
        if scroll > self.width:
            scroll=self.width
            
        if scroll != self.scroll_x:
            self.scroll_x=scroll
            self.draw()

    def scrolldown(self, e):
        scroll=self.scroll_y+SCROLL_STEP
        if scroll > self.height:
            scroll=self.height
        
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
