from biosppy.signals import ecg
import csv
import datetime
import pyedflib
from pyhrv.frequency_domain import welch_psd


def index_from_string(date_value, time_value, sampling):
    tmp = time_value.split(':')
    instant = datetime.datetime(date_value.year, date_value.month, date_value.day,
                                int(tmp[0]), int(tmp[1]), int(tmp[2]))

    if (instant-start_time).total_seconds() < 0:
        instant = datetime.datetime(date_value.year, date_value.month, date_value.day+1,
                                    int(tmp[0]), int(tmp[1]), int(tmp[2]))

    return int((instant-start_time).total_seconds()) * sampling


with pyedflib.EdfReader("data/n1.edf") as f:
    values = f.readSignal(12)
    start_time = f.getStartdatetime()
    sample_frequency = f.getSampleFrequency(12)

results = {
    "S1": [],
    "S2": [],
    "S3": [],
    "S4": []
}
with open("data/n1.out") as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    for line in reader:
        typ = line["Stage"]
        start = index_from_string(start_time, line["Start Instant"], sample_frequency)
        end = index_from_string(start_time, line["End Instant"], sample_frequency)

        if end-start > (sample_frequency*120):
            out = ecg.ecg(signal=values[start:end], sampling_rate=sample_frequency, show=False).as_dict()
            peaks = ecg.correct_rpeaks(signal=values[start:end], rpeaks=out["rpeaks"],
                                       sampling_rate=sample_frequency).as_dict()

            list_peaks = []
            for el in peaks['rpeaks']:
                list_peaks.append(int(el))

            res = welch_psd(rpeaks=list_peaks, show=False, show_param=False).as_dict()
            results[typ].append(round(res["fft_ratio"], 2))

for el in results:
    print(el, results[el])

