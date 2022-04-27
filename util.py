#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'
import logging
import random
from faker import Faker
import time
import datetime
import os
from hashlib import md5
LOG_LEVEL = logging.INFO

fake = Faker('zh_CN')

# 定义检查部门  'TPL':'病理科室','ECG':'心电科室','LIS':'检验科室','RAD':'放射科室','US':'超声科室','NM':'核医学','ES':'内镜'
# '放射科','超声科','康复科','急诊科','中医科','检验科','心电科','病理科','放射一科','放射二科'
# 'SC','CT','MR','DR','MR','US'，'ECG'
# PatientType_list = ['00', '10', '11', '20', '21', '22']
# BodyPart_list = ['头部', '胸部', '肺部', '脾脏', '肾脏', '甲状腺体']
# modality
# modality:  CT/MR/PT/US/XA/ECG/JPEG/Video
# blood test，pathological diagnosis BT和PD

class Log:
    """
    日志类：目前是控制台输出，有需要可以加文本输出handler
    """
    @staticmethod
    def _console(level, message):
        # 创建一个logger
        logger = logging.getLogger()
        logger.setLevel(LOG_LEVEL)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(LOG_LEVEL)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(ch)
        # 记录一条日志
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(ch)

    def debug(self, message):
        self._console('debug', message)

    def info(self, message):
        self._console('info', message)

    def warning(self, message):
        self._console('warning', message)

    def error(self, message):
        self._console('error', message)


def get_pat_basic_info():
    """
    生成患者基本信息：PatientID、PatientName、IdCardNo、PatientSex、Age、Birthday、InsuranceId、PhoneNumber
    :return: 信息字典
    """
    result = {
        'PatientID': f"PID{time.strftime('%Y%m%d')}{fake.random_number(5)}",
        'PatientName': fake.name(),
        'IdCardNo': fake.ssn(),
        'InsuranceId': f'Y{fake.random_number(8, fix_len=True)}',
        'PhoneNumber': fake.phone_number()
    }
    result['PatientSex'] = '1' if int(result['IdCardNo'][-2]) % 2 else '2'
    result['Age'] = str(time.localtime().tm_year - int(result['IdCardNo'][6:10]))
    result['Birthday'] = f'{result["IdCardNo"][6:10]}-{result["IdCardNo"][10:12]}-{result["IdCardNo"][12:14]}'
    return result


def get_uid(uid_type):
    """
    生成各类uid：StudyInstanceUID、SeriesInstanceUID、SOPInstanceUID
    :return: 按输入类型返回uid字符串
    """
    uid_limit = {
        'StudyInstanceUID': {'max': 200, 'min': 100},
        'SeriesInstanceUID': {'max': 500, 'min': 200},
        'SOPInstanceUID': {'max': 999, 'min': 500}
    }
    max_value = uid_limit.get(uid_type)['max']
    min_value = uid_limit.get(uid_type)['min']
    uid = f'1.{fake.random_digit()}.{fake.random_int(max=max_value, min=min_value)}.' \
          f'{fake.random_number(6, fix_len=True)}.{fake.random_number(12, fix_len=True)}.' \
          f'{fake.random_number(3, fix_len=True)}.{time.strftime("%Y%m%d%H%M%S")}' \
          f'{fake.random_number(6, fix_len=True)}.{fake.random_digit()}.{fake.random_digit()}'

    return uid


def get_study_basic_info():
    """
    生成各类检查基本信息：AccessionNumber、StudyInstanceUID
    :return: 信息字典
    """
    result = {
        'AccessionNumber': f'ANO{time.strftime("%Y%m%d")}{fake.random_number(6, fix_len=True)}',
        'StudyInstanceUID': get_uid('StudyInstanceUID')
    }
    return result


def get_report_basic_info():
    """
    生成报告动态信息：ReportDoctorName、AuditDoctorName、ApplyDoctor、ReportID、HisApplyNo、HisMedCardNo
    :return: 信息字典
    """
    result = {
        'ReportDoctorName': fake.name(),
        'AuditDoctorName': fake.name(),
        'ApplyDoctor': fake.name(),
        'ReportID': f'RepID{time.strftime("%Y%m%d")}{fake.pystr(max_chars=7)}',
        'HisApplyNo': f'HIS{fake.random_number(5, fix_len=True)}||{fake.random_number(3, fix_len=True)}',
        'HisMedCardNo': f'HIS_CARD{fake.random_number(5, fix_len=True)}'
    }
    return result


def get_report_file(filepath):
    """
    根据文件路径返回文件基本信息
    :param filepath: 文件路径
    :return: file/file_type/file_size/file_md5/file_name字典
    """
    md5sum = md5()
    file_name = os.path.basename(filepath)
    file_type = os.path.splitext(file_name)[-1][1:]
    with open(filepath, 'rb') as f:
        byte = f.read()
        md5sum.update(byte)
        file_md5 = md5sum.hexdigest()
    result = {
        'File': (file_name, open(filepath, 'rb').read()),
        'FileType': file_type if file_type != 'jpg' else 'jpeg',
        'FileSize': os.path.getsize(filepath),
        'FileMd5': file_md5,
        'FileName': file_name
    }
    return result


def get_times(time_count, max_delay=7, min_delay=0, formatting='%Y-%m-%d %H:%M:%S'):
    """
    生成时间信息：StudyTime list
    :return: 信息字典
    """
    if time_count > max_delay - min_delay:
        time_count = max_delay - min_delay
    now = datetime.datetime.now()
    time_list = random.sample(range(min_delay, max_delay+1), time_count)
    for t in time_list:
        calc_time = now - datetime.timedelta(days=t)
        yield calc_time.strftime(formatting)


# "StudyTime": "2021-07-19 17:18:00",
# "ApplyDatetime": "2021-07-16 09:00:00",
# "ArrivedDatetime": "2019-04-01 09:00:00",
# "AuditDatetime": "2019-04-01 09:00:00",
# "PrintDatetime": "2019-04-01 09:00:00",
# "VerifyDatetime": "2019-04-01 09:00:00"


if __name__ == '__main__':
    print(get_pat_basic_info())
    for i in get_time(5):
        print(i)
