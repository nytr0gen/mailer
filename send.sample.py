#!/usr/bin/python

import smtp
s = smtp.smtp()
## dig mx google.com
s.connect("aspmx.l.google.com", 25)
# s.connect("aspmx.l.google.com", 25, bindIP="127.0.0.1")
s.ehlo("test")
s.recv()
s.mailfrom("test@test.com")
s.to("nytr0gen.george@gmail.com")
s.data()

hey_buddy = "hey buddy!!!"
s.set_body_from_file("mail.sample", globals())
s.send_data()

print s.quit()
