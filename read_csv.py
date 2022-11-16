import os
import csv

def read_csv_header(filename):
    with open(filename) as f:
        f_reader = csv.reader(f)
        header = next(f_reader)
    return(header)

def read_csv_data(filename):
    with open(filename) as f:
        f_reader = csv.reader(f)
        header = next(f_reader)
        # data_dict = {}
        # for name in header:
        #     data_dict[name] = []
        data_dict = {key:[] for key in header}
        for i, row in enumerate(f_reader):
            for j, name in enumerate(header):
                try:
                    data = float(row[j])
                except ValueError:
                    data = row[j]
                data_dict[name].append(data)
    return data_dict
