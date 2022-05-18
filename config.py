#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

import socket
import os

BASE_DIR = os.path.dirname(__file__)

"""
EnvData: 环境参数
AeData： 环境AE参数
注意两个类中统一环境的key一致即可
"""


class EnvData:
    dev_api = {
        'cetus_url': 'https://cgs-dev-api.uihcloud.cn',
        'OrgCode': 'lc20200101',
        'LocationName': 'United-imaging Management',
        'auth_url': 'https://auth-dev-api.uihcloud.cn/',
        'token_client_id': 'D4qvWxbYPc6dy5fU',
        'token_client_secret': 'bf8871b718a2729eeaaac1d3d71528bdf4f8e9960a65dbce00197a6c78b4ad16',
        'ProcedureOffice': 'RAD'
    }
    mti_demo = {
        'cetus_url': 'http://10.6.5.244:30912',
        'OrgCode': 'lc20200101',
        'LocationName': 'United-imaging Management',
        'auth_url': 'http://shenzhou.10.6.5.244.sslip.io/auth',
        'token_client_id': 'k5bcwoA7XDmTWZ46',
        'token_client_secret': 'f1ff6b4244b29c0ee53c32952dc4d1228e7ac690f7e8dff8ee1495c17f034e2d',
        'ProcedureOffice': 'RAD'
    }


class AeData:
    dev_api = {
        'scp_ae': 'UIHHXZS67',
        'scp_ip': '10.2.58.9',
        'scp_port': 32610,
        'scu_ae': 'UIHPACSSERVER24',
        'scu_ip': socket.gethostbyname(socket.gethostname()),
        'scu_port': 3333
    }
    mti_demo = {
        'scp_ae': 'CGS_Server',
        'scp_ip': '10.6.5.244',
        'scp_port': 30911,
        'scu_ae': 'Fenix_App',
        'scu_ip': socket.gethostbyname(socket.gethostname()),
        'scu_port': 3333
    }


class ReportData:
    """
    定义report初始化参数
    """
    # cetus上传报告参数
    Data = {
        "OrgCode": "570796872",  # update字段
        "StudyInstanceUID": "1.2.156.112605.274973444419568.7416.20210726002.1",  # update字段
        "AccessionNumber": "AC20210726002",  # update字段
        "PatientID": "PT20210726002",  # update字段
        "PatientName": "test_gcl004",  # update字段
        "ReportID": "RPT20210726002",  # update字段
        "HasImage": "0",  # update字段
        "StudyTime": "2021-07-19 17:18:00",  # update字段
        "ProcedureOffice": "RAD",  # update字段
        "Modality": "MR",  # update字段
        "LocationName": "United-imaging Management",  # update字段
        "Age": "22",  # update字段
        "AgeUnit": "Y",
        "Birthday": "2000-04-01",  # update字段
        "Sex": "2",  # update字段
        "IdCardNo": "420101199901010045",  # update字段
        "PatientType": "04",
        "VisitType": "1",
        "PatientNo": "100",
        "MedicalHistory": "无",
        "ClinicalDiagnosis": "无",
        "ClinicalSymptom": "无",
        "ApplyOffice": "内分泌科",
        "ApplyDoctor": "张医师",  # update字段
        "ProcedureName": "腹部CT",
        "BodyPart": "头部",
        "ReportDoctorName": "张三",  # update字段
        "ReportDatetime": "2021-11-20 09:00:00",
        "ImageDescription": "影像描述/检查所见:测试接口返回影像描述信息，限制20个字符长度",
        "Conclusion": "影像诊断/检查提示：测试接口返回诊断意见相关信息，限制30个字符长度Ab1!@#$%^&*()",
        "Positive": "1",
        "Price": "1233",
        "PhoneNumber": "13585523117",  # update字段
        "InsuranceId": "A123456",  # update字段
        "CheckInfectDis": "肺结核",
        "BedNo": "A1234-4",
        "Spelling": "",
        "Race": "汉",
        "Passport": "",
        "DriveLicense": "",
        "CompanyAddress": "武汉市洪山区高新大道818号",
        "HomeAddress": "武汉市江岸区沿江大道188号",
        "HomeTown": "武汉市江夏区文化大道99号",
        "StudyStatus": "R",
        "HisId": "a589240",  # update字段
        "CheckPurpose": "查看是否有结节",
        "ProcedureRequirement": "检查要求",
        "ApplyDatetime": "2021-07-16 09:00:00",
        "CheckOffice": "放射一科室",
        "ProcedureDoctor": "王五",
        "ProcedureRoom": "F1234",
        "PayType": "城镇医保",
        "HisApplyNo": "54683189",  # update字段
        "CreateDoctorName": "赵六",
        "ArrivedDatetime": "2019-04-01 09:00:00",
        "AuditDoctorName": "李四",
        "AuditDatetime": "2019-04-01 09:00:00",
        "PrintDatetime": "2019-04-01 09:00:00",
        "VerifyDatetime": "2019-04-01 09:00:00",
        "VerifyDoctor": "李四",  # update字段
        "ImagePrinted": "1",
        "PrintStatus": "0",
        "Grade": "影像质评",
        "DoctorAdvice": "医生建议",
        "ReportRemark": "报告备注",
        "CriticalShow": "0",
        "CriticalValues": "肝破裂",
        "AcrIndex": "12345678",
        "Icd10Index": "123456",
        "HisMedCardNo": "123456",  # update字段
        "DiseaseName": "abc"
    }


if __name__ == '__main__':
    print(BASE_DIR)
