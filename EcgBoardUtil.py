import numpy as np
import os
import neurokit2 as nk
from biosppy.signals import ecg
import biosppy as biosppy

#读取心电板测量数据
with open('datalog.txt', 'r') as f:
    dataList = []
    data = np.array(f.readlines())
    for d in data:
        if (d in ['\n', '\r\n'])  or ("ECG" in d ):
            pass
        else:
            parsed = d.split(',')
            dataList.append(float(parsed[5]))
    # print(dataList)
#设置采样频率
sample_rate = 250

#使用biosppy算法过滤数据
out = ecg.ecg(signal=dataList, sampling_rate=sample_rate, show=False)
print(np.array(out["filtered"]))

#取中间稳定的数据，具体开始和结束节点根据实际情况设置
ecg_signal = np.array(out["filtered"][5000:15000])

#使用biosppy算法分析过滤后的数据
out = ecg.ecg(signal=ecg_signal, sampling_rate=sample_rate, show=True)
# print(out)

#使用neurokit2算法获取PQRST特征点
_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=sample_rate)
signal, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=sample_rate, method="dwt", show=True,
                                      show_type='all')
#打印ECG特征点
print("waves:::", waves_peak)



