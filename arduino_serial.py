import serial
import time
import datetime

from logger_func import make_logger


def single_loop(serial: serial.Serial, logger=None):
    while True:
        if serial.in_waiting > 0:
            ret_data = serial.readline().decode("utf-8").rstrip()

            # check data_num
            ret_data_split = ret_data.split(",")

            if len(ret_data_split) > 5 and ret_data_split[0]=="data":
                if logger is not None:
                    logger.info(ret_data)
                else:
                    print(ret_data)


def main(log_name, serial_port, baud_rate):
    _date = datetime.datetime.now()
    _date = _date.strftime("%Y%m%d_%H%M%S")
    _log_fmt = '%(asctime)s,%(msecs)03d,[%(levelname).4s], %(message)s'

    logger = make_logger(file_name=f"{_date}_BME_{log_name}",
                         use_time_rotate=False,
                         fmt=_log_fmt)

    while True:
        # 接続
        try:
            comport = serial.Serial(serial_port,
                                    baudrate=baud_rate,
                                    timeout=1)
        except Exception as err:
            # 接続できない場合、60秒後に再接続
            logger.error(f'error in setup serial-port: {err}')
            time.sleep(60)
            continue

        # 測定
        try:
            single_loop(comport, logger)

        except KeyboardInterrupt:
            logger.debug(f'keyboard interrupt')
            return

        except Exception as err:
            logger.error(f'error in main-loop: {err}')

        finally:
            logger.debug(f'close serial-port')
            comport.close()

        # 測定できない場合、60秒後に再接続
        time.sleep(60)


if __name__ == '__main__':
    main(log_name="",
         serial_port="COM5",
         baud_rate=115200)
