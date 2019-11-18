import pinyin
import pandas as pd
import os
from django.conf import settings
from copy import deepcopy


class HanZiToPinYin:
    """
    1 汉字转拼音： 黎明明 --> Mingming Li
    2 复制一份新文件，添加一列：【拼音】
    """
    def __init__(self, filename):
        self.origin_excel = os.path.join(settings.REPOSITORY_ROOT, 'data', 'recipients_sample.xlsx')
        self.new_filename = filename
        self.destination_excel = self._create_newfile()

    @staticmethod
    def hanzi_to_pinyin(name):
        if isinstance(name, str):
            part = pinyin.get(name, format="strip", delimiter=",").split(',')
            return " ".join([''.join(part[1:]).capitalize(), part[0].capitalize()])
        else:
            return " "

    def _create_newfile(self):
        """
        拼接新文件路径
        :return:
        """
        file_path = os.path.join(settings.REPOSITORY_ROOT, 'data', self.new_filename)
        writer = pd.ExcelWriter(file_path)
        return writer

    def run(self):
        """

        :return:
        """
        data = pd.read_excel(self.origin_excel)
        data['拼音'] = None
        for i, row in data.iterrows():
            data.loc[i, '拼音'] = self.hanzi_to_pinyin(row['姓名'])
        data.to_excel(self.destination_excel, sheet_name='Sheet1', index=False, header=True)
        self.destination_excel.save()


if __name__ == "__main__":
    HanZiToPinYin('new.xlsx').run()

