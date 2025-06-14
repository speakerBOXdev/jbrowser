import socket
import ssl
import tkinter
import tkinter.font
from layout import *
from tag import *
from controls import *
from parser import *

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 12, 18
SCROLL_STEP = 100
class Browser:
    def __init__(self):

        self.width=WIDTH
        self.height=HEIGHT

        self.window = tkinter.Tk()

        self.build_header(self.window)

        self.canvas = tkinter.Canvas(self.window,
            width=self.width,
            height=self.height-50,
        )
        self.canvas.pack(fill="both",expand=True)


        self.controls=[]
        self.controls.append(ScrollBar())
        self.controls.append(ScrollBar(direction="horizontal"))
        #self.controls.append(Button(10, 10, 20, 5))


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

        self.display_list=[]
        self.max_x=0
        self.max_y=0

    def build_header(self, parent):

        self.header=tkinter.Frame(parent, height=25, width=self.width, bg="navy")
        self.header.place(x=0, y=0)
        self.header.pack(fill="x", expand=True)

        self.txturl=tkinter.Text(self.header,height=1, width=50)
        self.txturl.grid(row=0, column=0)
        #self.txturl.pack()
        self.refresh=tkinter.Button(self.header, width=5, text="Go", command=self.reload)
        self.refresh.grid(row=0, column=1)
        #self.refresh.pack()


    def reload(self):
        urlvalue=self.txturl.get("1.0", "end-1c")
        print("New URL:{}".format(urlvalue))
        url=URL(urlvalue)
        self.load(url)        

    def load(self, url):

        urlvalue=self.txturl.get("1.0", "end-1c")
        if urlvalue == "":
            self.txturl.insert(tkinter.END, url.value)

        self.response=url.request()
        parser =HTMLParser(self.response)
        nodes=parser.parse()
        print_tree(nodes)
        
        layout=Layout(nodes)
        self.window.title(layout.title)
        self.display_list=layout.display_list

        self.max_x=0
        self.max_y=0
        for x, y, c, f in self.display_list:
            if x > self.max_x: self.max_x=x
            if y > self.max_y: self.max_y=y

        self.max_x+=HSTEP
        self.max_y+=VSTEP
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        for x, y, c, f in self.display_list:

            if y < VSTEP + self.scroll_y: continue
            if y > self.scroll_y + self.height: continue
            
            if x > self.scroll_x + self.width: continue
            if x < HSTEP + self.scroll_x: continue
            
            text_x=x - self.scroll_x
            text_y=y - self.scroll_y
            self.canvas.create_text(text_x, text_y, text=c, font=f, anchor="nw")

        window=(self.width, self.height)
        max=(self.max_x, self.max_y)
        scroll=(self.scroll_x, self.scroll_y)

        for control in self.controls:
            if isinstance(control, ScrollBar): control.update(window, max, scroll)
            control.draw(self.canvas)
        
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
        self.scroll_y=self.max_y+VSTEP+VSTEP-self.height
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


        max=self.max_x+SCROLL_STEP-self.width
        if scroll > max:
            scroll=max

        if scroll != self.scroll_x:
            self.scroll_x=scroll
            self.draw()

    def scrolldown(self, e):
        scroll=self.scroll_y+SCROLL_STEP
        max=self.max_y+VSTEP+VSTEP-self.height
        if scroll > max:
            scroll=max
        
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

        self.value=url

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
    
def print_tree(node, indent=0):
    print(" " * indent, node)
    for child in node.children:
        print_tree(child, indent + 2)

if __name__ == "__main__":
    import sys
    url=sys.argv[1]
    Browser().load(URL(url))
    tkinter.mainloop()
