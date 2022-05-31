#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

import requests
from util import Log
from config import ReportData
from urllib3 import encode_multipart_formdata

logger = Log()


def send_report(report_file=None, **kwargs):
    """
    发送报告
    """
    # cetus修改report参数
    data = ReportData.Data
    report_url = kwargs.pop('cetus_url') + '/access/v1/report/'
    auth_url = kwargs.pop('auth_url')
    token_client_id = kwargs.pop('token_client_id')
    token_client_secret = kwargs.pop('token_client_secret')
    kwargs['Sex'] = kwargs.pop('PatientSex')
    kwargs['HisId'] = kwargs['OrgCode'] + kwargs['PatientID']
    is_auth = kwargs.pop('is_auth')
    # data中更新人员信息和检查相关信息
    data.update(kwargs)
    if report_file:
        # 在data中增加文件信息
        data.update(report_file)
    # 转换data数据的类型为format
    encode_data = encode_multipart_formdata(data)
    # 请求format
    data = encode_data[0]
    logger.info(f'--报告参数整理完成，准备发送报告请求,modality:{kwargs.get("Modality")} 检查时间:{kwargs.get("StudyTime")}--')
    # 请求头
    if is_auth:
        send_report_headers = {
            "Authorization": "Bearer {0}".format(get_token(auth_url, token_client_id, token_client_secret)),
            'Content-Type': encode_data[1]}
    else:
        send_report_headers = {'Content-Type': encode_data[1]}
    logger.debug(f'header: {send_report_headers}   url: {report_url}')
    res = requests.post(report_url, headers=send_report_headers, data=data)
    if res.status_code != 200:
        logger.error('--报告发送失败--')
        logger.error(res.content)
    else:
        logger.info(f'--报告发送成功--name:{kwargs["PatientName"]} AccessionNumber:{kwargs["AccessionNumber"]} StudyInstanceUID:{kwargs["StudyInstanceUID"]}')


def get_token(url, app_id, app_key):
    get_token_url = url + '/v2/connect/token'
    params_dic = {'client_id': app_id, 'client_secret': app_key,
                  'grant_type': 'client_credentials'}
    get_token_header = {'Content-Type': 'application/x-www-form-urlencoded'}
    res_post_get_token = requests.post(url=get_token_url, headers=get_token_header, params=params_dic)
    if res_post_get_token.status_code != 200:
        logger.error("环境获取token失败")
        access_token = r'--------'
    else:
        res_post_get_token.content.decode("utf-8")
        access_token = res_post_get_token.json()['access_token']
    return access_token


def send_attach():
    # TBD
    pass

