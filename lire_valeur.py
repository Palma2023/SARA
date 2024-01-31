import RPi.GPIO as GPIO

def read_value(pin_value):

    GPIO.setmode(GPIO.BOARD)
    # GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin_value, GPIO.IN)# configures physical pin 13 as an input.
    result = GPIO.input(pin_value)# reads the state of the input pin 13 (high or low) and stores the result in the variable result
    return(result)
    
    
    
    #Test : brancher = 1 , débrancher = 0 -> alarme.
    #print("The value of result is", result)

