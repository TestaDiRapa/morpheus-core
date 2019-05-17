from biosppy.signals import ecg
import csv
import datetime
import pyedflib
from pyhrv.frequency_domain import welch_psd


def index_from_string(date_value, time_value, sampling):
    tmp = time_value.split(':')
    instant = datetime.datetime(date_value.year, date_value.month, date_value.day, int(tmp[0]), int(tmp[1]), int(tmp[2]))
    return int((instant-start_time).total_seconds()) * sample_frequency


with pyedflib.EdfReader("data/n1.edf") as f:
    values = f.readSignal(12)
    start_time = f.getStartdatetime()
    sample_frequency = f.getSampleFrequency(12)

with open("data/n1.out") as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for line in reader:
        start = index_from_string(start_time, line["Start Instant"], sample_frequency)
        end = index_from_string(start_time, line["End Instant"], sample_frequency)

        out = ecg.ecg(signal=values[start:end], sampling_rate=sample_frequency, show=False).as_dict()
        peaks = ecg.correct_rpeaks(signal=values[start:end], rpeaks=out["rpeaks"],
                                   sampling_rate=sample_frequency).as_dict()


list_peaks = []
for el in peaks['rpeaks']:
    list_peaks.append(int(el))

res = welch_psd(rpeaks=list_peaks).as_dict()
for key in res:
    print(key, res[key])