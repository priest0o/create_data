#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

from config import EnvData, AeData, BASE_DIR
from util import *
import dicom_handle
import report_handle

# 环境列表
env_list = ('dev_api',)
# 指定环境
environ = 'dev_api'
# 环境参数
env_data = getattr(EnvData(), environ)
# ae参数
ae_data = getattr(AeData(), environ)

modality_list = ['CT', 'MR', 'US', 'PT', 'XA', 'ECG', 'DR', 'BT', 'PD', 'JPEG', 'Video']
no_img_modality = ('BT', 'PD', 'JPEG', 'Video')
logger = Log()


def main(pat_basic_info, study_basic_info, report_basic_info, has_image='1', modality=None,
         study_time=time.strftime("%Y-%m-%d %H:%M:%S"), report_file=None, img_path=None):
    if not modality:
        modality = random.choice(modality_list)
    if modality not in no_img_modality and has_image == '1':
        # 如果没有指定，随机获取一组对应modality文件夹的影像
        if not img_path:
            original_root = os.path.join(BASE_DIR, f'original_data{os.sep}{modality}')
            img_path = os.path.join(original_root, random.choice(os.listdir(original_root)))
        logger.info(f'修改{modality}影像，原始路径{img_path}')
        save_info = dicom_handle.create_new_study(img_path, PatientID=pat_basic_info['PatientID'],
                                                  PatientName=pat_basic_info['PatientName'],
                                                  PatientSex=pat_basic_info['PatientSex'], **study_basic_info)
        logger.info(f'归档{pat_basic_info["PatientName"]}{modality}影像，新文件路径{save_info[0]}，请稍候....')
        dicom_handle.c_store(save_info, ae_data)
    else:
        has_image = '0'
    # 如果未指定报告文件，则不带文件上传报告
    report_file_info = None
    if report_file:
        report_file_info = get_report_file(report_file)
    report_handle.send_report(report_file=report_file_info, **pat_basic_info,
                              **study_basic_info, **env_data, **report_basic_info, StudyTime=study_time,
                              Modality=modality, HasImage=has_image)


def create_demo(max_delay=365, study_count=15, custom_modality=None, **kwargs):
    # pat_info = {'PatientID': 'PID2022042646175', 'PatientName': '周飞', 'IdCardNo': '532502198107084243', 'PatientSex': '2', 'Age': '31', 'Birthday': '1981-07-08'}
    pat_info = get_pat_basic_info()
    time_list = get_times(study_count, max_delay=max_delay)
    # time_list = ['2022-02-22 15:00:00']
    for t in time_list:
        study_info = get_study_basic_info()
        report_info = get_report_basic_info()
        if custom_modality:
            modality = custom_modality
        else:
            try:
                modality = modality_list.pop(0)
            except IndexError:
                modality = random.choice(no_img_modality)
        report_path = r"/CT.pdf"
        if modality == 'JPEG':
            report_path = r"/BT.jpg"
        main(pat_info, study_info, report_info, study_time=t, modality=modality, report_file=report_path, **kwargs)


if __name__ == '__main__':
    """
    PS： 
        - 文件顶部需要定义环境env_list = ('dev_api',)config.py中的环境列表
        - environ指定env_list中的某个环境，根据环境获取参数
        
    参数说明 
    patient_count-患者数量
    study_per_patient-每个患者报告数量
    max_delay_days-检查时间返回（当日往前n天内）
    custom_modality
        - random：随机选择modality_list-no_img_modality
        - demo：demo演示数据，一次按modality_list造一个完整数据
        - 其他： 必须指定modality_list中的一个
    img_path：指定影像路径（现在支持文件夹，文件暂未支持），不知道根据modality去Original_data里面找一个
    has_image:
        - '0': 不要图像
        - '1': 带图像
    """
    patient_count = 1
    study_per_patient = 1
    max_delay_days = 7
    for i in range(patient_count):
        create_demo(max_delay_days, study_per_patient, custom_modality=None, img_path=None, has_image='0')
