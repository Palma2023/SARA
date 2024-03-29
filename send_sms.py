#send_sms.py

import serial
import time
import sara

#phone_number_Remi = '+33778523259'

def sendSms(phone_number):

    # Activation du port série
    phone = serial.Serial("/dev/ttyUSB2", baudrate=115200, timeout=1)

    phone.write(b'AT\r\n')
    time.sleep(2)

    phone.write(b'AT+CMGF=1\r\n')
    time.sleep(3)

    phone.write(b'AT+CNMI=2,1,0,0,0\r\n')
    time.sleep(2)

    #phone.write(b'AT+CMGS=\"+33780514005\"\r\n')
    #time.sleep(2)

    phone.write(f'AT+CMGS=\"{phone_number}\"\r\n'.encode())
    time.sleep(2)

    phone.write(b'ALERTE SURVEILLANCE EQUIPEMENT\r\n')  # message
    time.sleep(2)

    phone.write(b'\x1A')  # Envoi du SMS
    time.sleep(2)

#print("sending_sms")
#sendSms(phone_number_Remi)
#print("sms succesfully sent")

