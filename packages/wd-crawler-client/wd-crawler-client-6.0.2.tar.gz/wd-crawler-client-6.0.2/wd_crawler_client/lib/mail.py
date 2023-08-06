# -*- coding: utf-8 -*-
import smtplib
import traceback
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail(object):

    def __init__(self, host, port, user, password):
        self.user = user
        self.server = smtplib.SMTP_SSL(host, port)
        self.server.login(user, password)

    def send(self, to_users, subject, content, attach_name=None, attach_content=None):
        msg = MIMEMultipart()
        msg['From'] = Header(self.user, 'utf-8').encode()
        msg['To'] = Header(u';'.join(to_users), 'utf-8').encode()
        msg['Subject'] = Header(subject, 'utf-8').encode()
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        if attach_name and attach_content:
            attach = MIMEText(attach_content, 'base64', 'utf-8')
            attach["Content-Type"] = 'application/octet-stream'
            attach["Content-Disposition"] = 'attachment; filename="%s"' % attach_name
            msg.attach(attach)
        try:
            self.server.sendmail(self.user, to_users, msg.as_string())
        except Exception as e:
            print(e)
            traceback.print_exc()

    def __del__(self):
        self.server.quit()
