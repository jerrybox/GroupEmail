# coding=utf-8
import os
import pandas as pd

from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class GroupSms:
    """
    群发短信
    """
    def __init__(self, accessKeyId, accessSecret, regionId, templateCode, signName):
        self.accessKeyId = accessKeyId
        self.accessSecret = accessSecret
        self.regionId = regionId

        self.templateCode = templateCode
        self.signName = signName
        self.request = self._request()

        self.recipients_excel = os.path.join(settings.REPOSITORY_ROOT, 'data', 'recipients_sample.xlsx')

    @property
    def client(self):
        return AcsClient(self.accessKeyId, self.accessSecret, self.regionId)

    @staticmethod
    def _request():
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')
        return request

    def set_content(self):
        self.request.add_query_param('RegionId', "cn-hangzhou")
        self.request.add_query_param('SignName', self.signName)
        self.request.add_query_param('TemplateCode', self.templateCode)

    def get_recipients(self):
        """
        生成器返回：用户名，邮箱
        """
        sheet1 = pd.read_excel(self.recipients_excel)
        return {row['手机号'] for _, row in sheet1.iterrows()}

    def send(self):
        """
        检查是否发送成功并记录下失败的号码
        :param phonenumbers:
        :return:
        """
        phonenumbers = self.get_recipients()

        self.set_content()
        for phone in phonenumbers:
            if not pd.isnull(phone):
                self.request.add_query_param('PhoneNumbers', int(phone))
                sms_response = self.client.do_action_with_exception(self.request)
                print(str(sms_response, encoding='utf-8'))


def send_sms():
    group_sms = GroupSms(
        "dfdfgdgfdgfgfgfgdfgdfgd",
        "dfgdfgdfgdfgdgfggf",
        "cn-hangzhou",
        "SMS_1774564879407",
        "奥特思鼎",
    )
    group_sms.send()
