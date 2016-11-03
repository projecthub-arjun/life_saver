# Library for using delay
import time

# library to communicate with arduino
# through serial (USB)
import serial

# Class to communicate with arduino
class Sensor:
    # Initialize the serial port
    def __init__(self, device = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0', baud_rate = 9600, debug_print = False):
        self.device = device
        self.baud_rate = baud_rate
        self.debug_print = debug_print
        self.ser = serial.Serial(self.device, self.baud_rate)
        self.ser.flushInput()
        self.ser.flushOutput()
        time.sleep(2)

    # Read the serial data from arduino and parse the sensor data
    def get_sensor_data(self):
        raw_sensor_data = self.ser.readline().strip("\r\n")

        if(self.debug_print):
            print raw_sensor_data

        sensor_data_list = raw_sensor_data.split(" ")

        acc_x = int(sensor_data_list[0].split("Acc:")[1])
        lat = str(sensor_data_list[1].split("Lat:")[1])
        lon = str(sensor_data_list[2].split("Lon:")[1])

        return acc_x, lat, lon

    # Close the serial port on exit
    def __del__(self):
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.close()

def main():
    arduino_ser = Sensor(debug_print = False)
    while(True):
        try:
            print arduino_ser.get_sensor_data()
        except:
            pass

# Start of execution
if __name__ == '__main__':
    main()
