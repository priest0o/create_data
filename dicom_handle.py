#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

import os
from itertools import product
from xpinyin import Pinyin
from collections import defaultdict
from pydicom import dcmread
from tqdm import tqdm
from pynetdicom import AE, build_context, sop_class
from util import Log, get_uid
from config import BASE_DIR

logger = Log()
pinyin = Pinyin()


# debug_logger()
def c_store(save_info, ae_config):
    """
    归档影像到对应的AE
    :param save_info: [文件夹, media_storage_sop_class_uid, transfer_syntax_uid]
    :param ae_config: AE信息字典
    :return:
    """
    filepath, media_storage_sop_class_uid_list = save_info
    scu_ae = ae_config['scu_ae']
    scp_ae = ae_config['scp_ae']
    scp_ip = ae_config['scp_ip']
    scp_port = ae_config['scp_port']
    ae = AE(scu_ae)
    logger.debug(f'local_ae_title: {scu_ae}, scp_ae_connect: {scp_ae}/{scp_ip}/{scp_port}')
    for media_storage_sop_class_uid in media_storage_sop_class_uid_list:
        ae.requested_contexts.append(build_context(media_storage_sop_class_uid))
    ae.requested_contexts.append(build_context('1.2.840.10008.5.1.4.1.1.1'))
    assoc = ae.associate(scp_ip, scp_port, ae_title=scp_ae)
    if not assoc.is_established:
        logger.error('Association rejected, aborted or never connected')
        raise ConnectionError
    logger.info('DICOM server init success')
    logger.info('start c-store')
    for root, path, files in os.walk(filepath):
        for file in tqdm(files, desc='归档中....'):
            file_path = os.path.join(root, file)
            ds = dcmread(file_path, force=True)
            assoc.send_c_store(ds)
    logger.info('c-store finish')
    assoc.release()


def create_new_study(filepath, **kwargs):
    """
    根据原始文件构造新文件
    :param filepath: 原始文件路径（文件夹）
    :param kwargs: 需要替换的tag字典
    :return: 新文件路径（文件夹）、c-store需要的media_storage_sop_class_uid, transfer_syntax_uid
    """
    logger.info(f"create {kwargs.get('PatientName')} study {kwargs.get('StudyInstanceUID')} start")
    # 根据患者信息和检查id新建路径
    save_root_dir = os.path.join(BASE_DIR, f"save_root_dir{os.sep}{kwargs.get('PatientName')}_"
                                           f"{kwargs.get('PatientID')}{os.sep}{kwargs.get('StudyInstanceUID')}")
    os.makedirs(save_root_dir)
    # 原始文件series字典
    series_dict = defaultdict(int)
    series_uid = ''
    save_path = ''
    media_storage_sop_class_uid_list = set()
    series_num = kwargs.pop('SeriesNum')
    img_num = kwargs.pop('ImgNum')
    # 汉字转拼音，避免dicom文件编码问题导致dicom显示名字乱码
    if kwargs.get('PatientName', None):
        kwargs['PatientName'] = pinyin.get_pinyin(kwargs['PatientName'], splitter=' ').title()
    if os.path.isdir(filepath):  # 遍历原始文件生成新文件
        for root, path, files in os.walk(filepath):
            for file in tqdm(files, desc='生成新检查中....'):
                if not file.endswith('dcm'):
                    continue
                file_path = os.path.join(root, file)
                ds = dcmread(file_path, force=True)
                try:
                    media_storage_sop_class_uid_list.add(ds.file_meta.MediaStorageSOPClassUID)
                except AttributeError:
                    logger.warning(f'{file} has no attribute MediaStorageSOPClassUID')
                try:
                    original_series = ds['SeriesNumber'].value
                except KeyError:
                    logger.warning(f'{file} has no attribute SeriesNumber, 丢弃')
                    continue
                sop_uid = get_uid('SOPInstanceUID')
                if not series_dict[original_series]:
                    series_dict[original_series] += 1
                    series_uid = get_uid('SeriesInstanceUID')
                    save_path = os.path.join(save_root_dir, series_uid)
                    os.mkdir(save_path)
                kwargs.update({'SeriesInstanceUID': series_uid, 'SOPInstanceUID': sop_uid})
                try:
                    for tag, value in kwargs.items():
                        ds[tag].value = value
                    ds.save_as(os.path.join(save_path, f'{sop_uid}.dcm'), write_like_original=False)
                except Exception as e:
                    logger.error(e)
    elif os.path.isfile(filepath):  # 基于单文件生成
        if not filepath.endswith('dcm'):
            raise ValueError(f'{filepath} is not dcm file')
        ds = dcmread(filepath, force=True)
        product_nums = product(range(1, series_num+1), range(1, img_num+1))
        media_storage_sop_class_uid_list.add(ds.file_meta.MediaStorageSOPClassUID)
        for s, i in tqdm(list(product_nums), desc='生成新检查中....'):
            sop_uid = get_uid('SOPInstanceUID')
            if not series_dict[s]:
                series_dict[s] += 1
                series_uid = get_uid('SeriesInstanceUID')
                save_path = os.path.join(save_root_dir, series_uid)
                os.mkdir(save_path)
            kwargs.update({'SeriesInstanceUID': series_uid, 'SOPInstanceUID': sop_uid,
                           'SeriesNumber': s, 'InstanceNumber': i})
            try:
                for tag, value in kwargs.items():
                    ds[tag].value = value
                ds.save_as(os.path.join(save_path, f'{sop_uid}.dcm'), write_like_original=False)
            except Exception as e:
                logger.error(e)
    else:
        raise ValueError(f'{filepath} is not found')
    if not media_storage_sop_class_uid_list:
        raise ValueError('There is no MediaStorageSOPClassUID, unable to continue c-store')
    logger.info(f"create {kwargs.get('PatientName')} study {kwargs.get('StudyInstanceUID')} finish")
    return save_root_dir, media_storage_sop_class_uid_list


if __name__ == '__main__':
    pass
