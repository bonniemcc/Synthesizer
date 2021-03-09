""" Code to have the synthesizer playing more than 1 note at the
	same time. This means the synthesizer can detecrt two or more 
	buttons being pressed at the same time.
"""

#Import useful packages
from webiopi.devices.digital.mcp23XXX import MCP23S17
from webiopi.devices.analog.mcp3x0x import MCP3208
import webiopi
GPIO=webiopi.GPIO
import time
import os
import numpy as np

# Setup chip 1
mcp = MCP23S17(chip=0, slave=0x20)

# Setup chip 2
mcp2 = MCP23S17(chip=1, slave=0x21) 


#Loops over all 10 buttons and sets them up
#At start have 8 buttons labelled 0-8
for i in range(0,10):
	mcp.setFunction(i, GPIO.IN)
mcp.setFunction(10, GPIO.OUT)

#Create numpy array to set up the 8 LEDs
LED = np.arange(0, 8, 1)

#Sets all 8 LED pins as outputs
for i in range(0,8):
	mcp2.setFunction(i, GPIO.OUT)
	mcp2.digitalWrite(i, GPIO.HIGH)

#Sound list
sound = ['aplay -q C5.wav &', 'aplay -q C#5.wav &', 'aplay -q A5.wav &', 'aplay -q A#5.wav &', 'aplay -q B5.wav &', 'aplay -q B6.wav &', 'aplay -q G5.wav &', 'aplay -q E5.wav &']

while True:
	
	#Set up switch register and print (integer value)
	switch_register = mcp.portRead()
	print(switch_register)
	
	#Write the integer as binary list, used to debug
	string = '{0:010b}'.format(switch_register)
	print(string)
	
	#Numpy array of all zeros
	switch = np.zeros(10)
	
	#Code to register which buttons are being pressed
	for i in range(10):
		if string[i] == '1':
			switch[9-i] = 1
	
	for i in range (0, 8):
		for j in range(0, 8):
			if (switch[i] == True and switch[j] == True):
				os.system(sound[i])
				os.system(sound[j])
				time.sleep(0.2)
				mcp2.digitalWrite(LED[i], GPIO.LOW)
				mcp2.digitalWrite(LED[j], GPIO.LOW)
				time.sleep(0.2)
				switch[i] =  False
				switch[j] = False
				mcp2.digitalWrite(LED[i], GPIO.HIGH)
				mcp2.digitalWrite(LED[j], GPIO.HIGH)

	time.sleep(1)
	
	
	
	
	

