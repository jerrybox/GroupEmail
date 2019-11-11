
### Package
* django-2.2
* pandas-0.25.3
* xlrd-1.2.0


### 发邮件注意事项：

1. 群发邮件：
    - 群发邮件会在收件人这一列看到所有的人的邮箱，从而泄露其他账户的信息
    - 为了保护其他人的账户信息，只能单独发给每一个人
    ```html
    my subject
    
    发件人：sdfsfdsf <sdfsfsde@sdfsdfsf.com>    	
    时   间：2019年11月11日(星期一) 中午11:38	纯文本 |  
    收件人：
    Jerry <996067941@qq.com>; sdfsfsfsf <sdfsfsf@sdfsfsdu.com>; fake <fake@example.com>
    附   件：
    1 个 (终稿2019年9月10日.pdf)
    ```

2. 发邮件后无法判断邮件是否成功投递
    - [参考1](https://stackoverflow.com/questions/2342456/how-to-check-if-the-mail-has-been-sent-successfully)
    - [参考2](https://unix.stackexchange.com/questions/179205/is-there-any-way-to-check-email-sent-success-acknowledgement)

3. 各邮箱服务商对个人邮箱每日发送的邮件数量有限制，注意查看退件


### [群发邮件参考](https://www.jb51.net/article/34498.htm)


### [发送邮件代码](https://www.tutorialspoint.com/django/django_sending_emails.htm)

0. 发送纯文本：
```python
from django.core.mail import send_mail
from django.conf import settings
def group_email():
    send_mail(
        'Subject here',
        'Here is the message.',
        settings.EMAIL_HOST_USER,
        ['996067941@qq.com'],
        fail_silently=False,
    )
```

1. 发送html message
```python
from django.core.mail import EmailMessage
def send_html_email():
   html_content = "<strong>Comment tu vas?</strong>"
   email = EmailMessage("my subject", html_content, settings.EMAIL_HOST_USER, ['996067941@qq.com'])
   email.content_subtype = "html"
   res = email.send()
```

2. 发送html message 带附件
```python
import os

from django.conf import settings

from django.core.mail import EmailMessage


def send_email_with_attach():
    html_content = "Comment tu vas?"
    email = EmailMessage("my subject", html_content, settings.EMAIL_HOST_USER, ['996067941@qq.com'])
    email.content_subtype = "html"  # Main content is text/html
    
    
    attach_file_path = os.path.join(settings.MEDIA_ROOT, 'attach', '终稿2019年9月10日.pdf')
    email.attach_file(attach_file_path)

    res = email.send()
    print(res)
```

3. 发送邮件 正文带图片，附件带pdf
```python
import os

from email.mime.image import MIMEImage

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email_with_attach():

    # 主题：
    subject = "Invitation"

    # 接受对象：
    recipients = ['996067941@qq.com', 'niuxisdfsdfsie@sdfsdfsu.com', 'fake@example.com']

    # 内文上下文变量
    image_file_name = 'logo.png'
    pdf_file_name = '终稿2019年9月10日.pdf'
    context = {"name": "Jerry", "image_file_name": image_file_name}

    # 富文本内容
    html_content = render_to_string('email/groupemail.html', context=context).strip()

    # 构建对象
    email = EmailMultiAlternatives(subject, html_content, settings.EMAIL_HOST_USER, recipients)
    email.content_subtype = "html"  # Main content is text/html
    email.mixed_subtype = 'related'  # This is critical, otherwise images will be displayed as attachments!

    # 正文附图
    image_path = os.path.join(settings.MEDIA_ROOT, 'email/images', image_file_name)
    image_file = open(image_path, 'rb').read()
    image = MIMEImage(image_file)
    image.add_header('Content-ID', '<{}>'.format(image_file_name))
    email.attach(image)

    # 添加附件
    attach_file_path = os.path.join(settings.MEDIA_ROOT, 'email/attach', pdf_file_name)
    email.attach_file(attach_file_path)

    # 发送
    res = email.send()
    print(res)
```

4. 



### Test shell
```python
>>> python manage.py shell
>>> from GroupEmail.apps.spam.views import send_email_with_attach
>>> send_email_with_attach()
Email [996067941@qq.com] was sended with result code: 1
Email [dsdfsdfsdfse@sdfsdfsfdu.com] was sended with result code: 1
Email [faker@example.com] was sended with result code: 1
Email [gsdfdsfe@sdfsdfdu.com] was sended with result code: 1
Email [innomal@ example.com] was sended with result code: 1
Email [qisdfdsfdeng@sdfsdfdu.com] was sended with result code: 1
>>> exit()

```


### [Django Settings](https://docs.djangoproject.com/en/2.2/ref/settings/)



### [Sending email](https://docs.djangoproject.com/en/2.2/topics/email/)


### [Sending Emails With Django Templates Stored in a Database](https://blog.anvileight.com/posts/django-email-templates-with-context-stored-in-database/)


