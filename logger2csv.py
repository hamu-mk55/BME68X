import os
import csv
import glob

SENSOR_NUM = 9


def convert_single_file(log_file: str, out_file: str):

    fw = open(out_file, 'a')
    csvWriter = csv.writer(fw, lineterminator='\n')

    log = open(log_file, 'r')
    for _line in log:
        _items = _line.rstrip().split(",")

        # センサ出力データかどうか確認
        if len(_items) < 8 + SENSOR_NUM:
            continue

        if "INFO" not in _items[3] or "data" not in _items[4]:
            continue

        # CSV出力
        row = [os.path.basename(log_file)] + _items[0:3] + _items[5:]

        csvWriter.writerow(row)

    log.close()
    fw.close()


def convert_logfile(log_dir: str = './log', out_file: str = "test.csv"):
    fw = open(out_file, 'w')
    csvWriter = csv.writer(fw, lineterminator='\n')
    csvWriter.writerow(["file",
                        "date",
                        "time",
                        "msec",
                        "temp",
                        "humid",
                        "press",
                        "sensor1",
                        "sensor2",
                        "sensor3",
                        "sensor4",
                        "sensor5",
                        "sensor6",
                        "sensor7",
                        "sensor8",
                        "sensor9",
                        ])
    fw.close()

    logfiles = glob.glob(f'{log_dir}/*.log*')

    for logfile in logfiles:
        if not os.path.isfile(logfile):
            continue

        convert_single_file(logfile, out_file)


if __name__ == '__main__':
    convert_logfile()
