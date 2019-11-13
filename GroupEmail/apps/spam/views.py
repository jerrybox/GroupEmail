import logging
import os
from time import sleep

from email.mime.image import MIMEImage

import pandas as pd

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


class Spam:
    """
    群发独显邮件：
    1 文件中读取邮箱与姓名
    2 批量发送但是收件人处只显示收件人自己的邮箱
    """

    def __init__(self):
        self.subject = "2019国际创新创业教育论坛邀请函"
        self.from_email = settings.EMAIL_HOST_USER
        self.email_template ='email/groupemail.html'
        self.image_filename = 'oustandinglog.png'
        self.pdf_filename = '2019国际创新创业教育峰会邀请函(11-17 成都）.pdf'
        self.default_name = 'default'

        self.recipients_excel = os.path.join(settings.REPOSITORY_ROOT, 'data', 'recipients_sample.xlsx')
        self.attach_file_dir = os.path.join(settings.MEDIA_ROOT, 'email', 'attach')
        self.image_dir = os.path.join(settings.MEDIA_ROOT, 'email', 'images')

    def attach_image_inline(self, image_file_name):
        image_path = os.path.join(self.image_dir, image_file_name)
        image_file = open(image_path, 'rb').read()
        image = MIMEImage(image_file)
        image.add_header('Content-ID', '<{}>'.format(image_file_name))
        return image

    def get_recipients(self):
        """
        生成器返回：用户名，邮箱
        """
        sheet1 = pd.read_excel(self.recipients_excel)
        return {(row['姓名'], row['邮箱']) for _, row in sheet1.iterrows()}

    def send(self):
        for name, email in self.get_recipients():
            html_content = render_to_string(self.email_template,
                                            context={'name': name if not pd.isnull(name) else self.default_name, "image_file_name": self.image_filename})
            html_email = EmailMultiAlternatives(self.subject, html_content, self.from_email, [email])
            html_email.content_subtype = "html"
            html_email.mixed_subtype = 'related'

            # 正文图片：
            html_email.attach(self.attach_image_inline(self.image_filename))

            # 附件文件：
            html_email.attach_file(os.path.join(self.attach_file_dir, self.pdf_filename))

            sleep(2)
            try:
                res = html_email.send()
                print("Email [{email}] was sent with result code: {res}".format(email=email, res=res))
            except Exception as e:
                print("Email {email} with error: {e}".format(email=email, e=e))


def send_email_with_attach():
    spam = Spam()
    spam.send()






