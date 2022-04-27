#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'cy'

from tqdm import tqdm
import os

n = 0
for i, j, k in os.walk(r'D:\4-script\study\create_data\original_data\MR\LTX_UIH_MR_血管'):
    for x in tqdm(k):
        n += 1
print(n)
