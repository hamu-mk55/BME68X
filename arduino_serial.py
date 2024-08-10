import serial
import time

from logger_func import make_logger


def main(log_name, serial_port, baud_rate):
    logger = make_logger(file_name=f"BME_{log_name}")

    comport = serial.Serial(serial_port,
                            baudrate=baud_rate,
                            timeout=1.0)

    try:
        while True:

            if comport.in_waiting > 0:
                ret_data = comport.readline().decode("utf-8").rstrip()

                ret_data_split = ret_data.split(",")

                if len(ret_data_split) > 5:
                    logger.info(ret_data)

    except KeyboardInterrupt:
        pass

    finally:
        comport.close()


if __name__ == '__main__':
    main(log_name="",
         serial_port="COM5",
         baud_rate=115200)
