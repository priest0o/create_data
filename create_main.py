#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

from glob import glob
from config import EnvData, AeData, BASE_DIR
from util import *
import dicom_handle
import report_handle

# 环境列表
env_list = ('dev_api', 'mti_demo')
# 指定环境
environ = 'dev_api'
# 环境参数
env_data = getattr(EnvData(), environ)
# ae参数
ae_data = getattr(AeData(), environ)

modality_list = ['CT', 'MR', 'US', 'PT', 'XA', 'ECG', 'DR', 'BT', 'PD', 'JPEG', 'Video']
modality_set = set(modality_list)
no_img_modality = ('BT', 'PD', 'JPEG', 'Video', 'ECG')
logger = Log()
root_report_path = os.path.join(BASE_DIR, 'report')


def main(pat_basic_info, study_basic_info, report_basic_info, has_image_status='1', modality=None,
         study_time=time.strftime("%Y-%m-%d %H:%M:%S"), report_file=None, img_info=None, auth=True,
         series_num=1, img_num=1):
    StudyDate = study_time.split(' ')[0]  # 待定
    StudyTime = study_time.split(' ')[1]  # 待定
    if not modality:
        modality = random.choice(modality_list)
    if modality in modality_set.difference(no_img_modality) and has_image_status == '1':
        # 如果没有指定，随机获取一组对应modality文件夹的影像
        if not img_info:
            original_root = os.path.join(BASE_DIR, f'original_data{os.sep}{modality}')
            img_info = os.path.join(original_root, random.choice(os.listdir(original_root)))
        logger.info(f'修改{modality}影像，原始路径{img_info}')
        save_info = dicom_handle.create_new_study(img_info, PatientID=pat_basic_info['PatientID'],
                                                  PatientName=pat_basic_info['PatientName'],
                                                  PatientSex=pat_basic_info['PatientSex'],
                                                  SeriesNum=series_num,
                                                  ImgNum=img_num,
                                                  **study_basic_info)
        logger.info(f'归档{pat_basic_info["PatientName"]}{modality}影像，新文件路径{save_info[0]}，请稍候....')
        dicom_handle.c_store(save_info, ae_data)
    else:
        has_image_status = '0'
    # 如果未指定报告文件，则不带文件上传报告
    report_file_info = None if not report_file else get_report_file(report_file)
    report_handle.send_report(report_file=report_file_info, **pat_basic_info,
                              **study_basic_info, **env_data, **report_basic_info, StudyTime=study_time,
                              Modality=modality, HasImage=has_image_status, is_auth=auth)


if __name__ == '__main__':
    """
    PS： 
        - 文件顶部定义了环境env_list = ('dev_api',)， 来源是config.py中配置的各个环境，列出来方便选择
        - environ指定env_list中的某个环境，根据环境获取参数

    参数说明 
    patient_count-患者数量
    study_per_patient-每个患者报告数量
    max_delay_days-检查时间前推最大天数（当日往前n天内）
    custom_modality
        - None：随机选择modality_list-no_img_modality
        - demo：demo演示数据，依次按modality_list造一个完整数据
        - 其他：自定义modality，不在modality_list-no_img_modality范围内的话不传图
    is_auth：是否需要通过uap鉴权
    img_path：指定影像路径
        - 未指定根据modality去Original_data里面找一个子文件夹
        - 指定文件夹则修改并上传文件夹下的所有dcm文件
        - 指定文件则配合series_per_study和image_per_series参数生成指定数量图像
    has_image:
        - '0': 不要图像
        - '1': 带图像
    has_report_file: 报告是否需要文件
    """
    patient_count = 1
    study_per_patient = 1
    max_delay_days = 0
    custom_modality = None
    is_auth = True
    img_path = None
    report_path = None
    has_image = '0'
    has_report_file = True
    """
    如果需要按自定义的一张图，自定义Series数量和Image数量，设置如下参数
    """
    series_per_study = 1
    image_per_series = 1

    for i in range(patient_count):
        pat_info = get_pat_basic_info()  # 随机获取患者基本信息
        time_list = get_times(study_per_patient, max_delay=max_delay_days)  # 获取过去max_delay_days天内，study_per_patient天的列表
        for t in time_list:
            study_info = get_study_basic_info()  # 随机获取检查基本信息
            if not custom_modality:  # 随机一个modality，modality_list-no_img_modality
                # current_modality = random.choice(list(modality_set.difference(no_img_modality)))
                current_modality = random.choice(modality_list)
            elif custom_modality == 'demo':  # demo数据，依次从modality_list选择创建数据
                try:
                    current_modality = modality_list.pop(0)
                except IndexError:
                    current_modality = random.choice(no_img_modality)
            else:  # 指定的modality字符串
                current_modality = custom_modality
            report_info = get_report_basic_info(current_modality)  # 随机获取报告基本信息
            report = None
            if has_report_file:
                if report_path:
                    report = report_path
                else:
                    match_reports = glob(os.path.join(root_report_path, f'{current_modality}*'))
                    report = match_reports[0] if match_reports else os.path.join(BASE_DIR, "CT.pdf")
            logger.debug(f'{t}报告文件路径{report}')
            main(pat_info, study_info, report_info, has_image_status=has_image, modality=current_modality,
                 study_time=t, report_file=report, img_info=img_path, auth=is_auth, series_num=series_per_study,
                 img_num=image_per_series)

"""
demo数据专用患者, 替换for循环中的随机患者和日期
    pat_info = {'PatientID': 'PID202205184239', 'PatientName': '演示', 'IdCardNo': '513430194711048539', 'InsuranceId': 'Y72120725', 'PhoneNumber': '15162075120', 'PatientSex': '1', 'Age': '75', 'Birthday': '1947-11-04'}
    time_list = ['2022-02-27 17:46:11', '2022-02-21 17:46:11', '2022-01-24 17:46:11', '2022-04-28 17:46:11',
                 '2022-01-09 17:46:11', '2020-11-20 17:46:11', '2022-03-14 17:46:11', '2020-09-08 17:46:11',
                 '2019-12-26 17:46:11',
                 '2020-11-02 17:46:11', '2020-11-18 17:46:11', '2020-12-12 17:46:11', '2022-03-21 17:46:11',
                 '2021-05-28 17:46:11',
                 '2021-01-29 17:46:11', '2020-10-17 17:46:11', '2022-02-17 17:46:11', '2020-12-03 17:46:11',
                 '2021-05-16 17:46:11',
                 '2020-01-28 17:46:11', '2022-04-20 17:46:11', '2020-06-04 17:46:11', '2020-03-16 17:46:11',
                 '2021-04-08 17:46:11',
                 '2020-08-18 17:46:11', '2022-03-06 17:46:11', '2021-02-01 17:46:11', '2021-05-11 17:46:11',
                 '2021-08-20 17:46:11',
                 '2021-03-09 17:46:11']
"""