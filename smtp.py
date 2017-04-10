import socket
import base64
import re

class smtp:
    def __init__(self):
        self.host = ""
        self.port = ""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.body = ""

    def send(self, cmd):
        self.s.sendall(cmd)

        print ["Sent: " + cmd]

    def recv(self):
        data = self.s.recv(1024)
        print ["Recv: " + data]

        return data

    def connect(self, host=0, port=0, bindIP=None):
        if host != 0:
            self.host = host
        if port != 0:
            self.port = port

        if bindIP:
            self.bindIP = bindIP
            self.s.bind((self.bindIP, 0))

        self.s.connect((self.host, self.port))
        # self.s.setblocking(False)

    def helo(self, host):
        self.send("HELO %s\r\n" % host)

        return self.recv()

    def ehlo(self, host):
        self.send("EHLO %s\r\n" % host)

        return self.recv()

    def auth(self, username, password):
        self.send("AUTH LOGIN\r\n")
        data = self.recv()

        if data[:3] != "334":
            return "1" + data

        self.send(base64.b64encode(username) + "\r\n")
        data = self.recv()

        if data[:3] != "334":
            return "2" + data

        self.send(base64.b64encode(password) + "\r\n")
        data = self.recv()

        return data

    def mailfrom(self, mail):
        self.send("MAIL FROM: <%s>\r\n" % mail)
        data = self.recv()

        return data

    def to(self, mail):
        self.send("RCPT TO: <%s>\r\n" % mail)
        data = self.recv()

        return data

    def data(self):
        self.send("DATA\r\n")
        data = self.recv()

        return data

    def set_body(self, body):
        self.body = body

    def set_body_from_file(self, file, vars=[]):
        f = open(file, "r")
        self.body = ""
        re_variables = re.compile(r"\$\{(.+?)\}")
        for line in f:
            matches = re_variables.findall(line)
            for var in matches:
                if var in vars:
                    line = line.replace("${%s}" % var, vars[var])
            self.body += line

        self.body = self.body.replace("\\r", "\r").replace("\\n", "\n")

        # TODO: maybe this is not desirable
        self.body = self.body.replace("\r\n", "\n").replace("\n", "\r\n")

    def send_data(self):
        self.send(self.body)
        data = self.recv()

        return data

    def quit(self):
        self.send("QUIT\r\n")
        data = self.recv()
        self.s.close()

        return data
