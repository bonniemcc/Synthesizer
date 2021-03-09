""" 
	Amy Paxton and Bonnie McCallion
	30th November 2018: Synthesizer Project C
	
	Code to have the synthesizer playing more than 1 note at the
	same time and added features to record and playback a tune and 
	control the volume using a variable resistor.
	
"""

#Import useful packages
from webiopi.devices.digital.mcp23XXX import MCP23S17
from webiopi.devices.analog.mcp3x0x import MCP3208
import webiopi
GPIO=webiopi.GPIO 
import time
import os
import numpy as np

#Setup MCP chip 1
mcp = MCP23S17(chip=0, slave=0x20)

#Set up ADC chip
ADC = MCP3208(chip=1)

#Loops over all 10 pushbuttons and set them up
#Buttons 0-9 are inputs and 10 is an LED output
for i in range(0, 10):
	mcp.setFunction(i, GPIO.IN)
mcp.setFunction(10, GPIO.OUT)

#Turn LED off initially
mcp.digitalWrite(10, GPIO.HIGH)

#Create list containing sounds which correspond to each pushbutton
sound = ['aplay -q E5.wav &', 'aplay -q F5.wav &', 'aplay -q F#5.wav &', 
			'aplay -q G5.wav &', 'aplay -q G#5.wav &', 'aplay -q A5.wav &', 
			'aplay -q A#5.wav &', 'aplay -q B5.wav &']

#Create empty list to store sounds to be played back
recording = []


#Loop forever
while True:
	
	#Read in the voltage of channel 0
	voltage = ADC.analogReadVolt(0)
	print("voltage is", voltage)
	
	#Set the volume using amixer
	volume = voltage * 40
	os.system("amixer set Master {}%".format(volume))

	#Reading the inputs of the pushbuttons as an integer
	switch_register = mcp.portRead()
	print(switch_register)
	
	#Write the integer as binary list
	string = '{0:011b}'.format(switch_register)
	print(string)
	
	#Numpy array of zeros, corresponding to no pushbuttons initially pressed
	switch = np.zeros(11)
	
	#Code to register which buttons are being pressed
	#Loop over all pushbuttons and use binary string to detect when pushbutton is on
	for i in range(11):
		if string[i] == '1':
			switch[10-i] = 1
	print(switch)
	
	#Whilst the recording button is being held
	if switch[8] == True:

		#Turn LED on to indicate recording
		mcp.digitalWrite(10, GPIO.LOW)
		
		#Loop over first 8 (sound) buttons
		for i in range (0, 8):
			if switch[i] == True:
				#Play sound corresponding to button being pressed
				os.system(sound[i])
				#Append sound to recording list to be played back
				recording.append(sound[i])
				time.sleep(0.2)
				#Turn button off
				switch[i] =  False
				time.sleep(0.2)
		#Turn recording button and LED off
		switch[8] = False
		mcp.digitalWrite(10,GPIO.HIGH)
	
	#Whilst playback button is being held
	if switch[9] == True:
		for i in range(len(recording)):
			os.system(recording[i])
			time.sleep(0.5)
		#Turn playback button off
		switch[9] = False
		recording = []
					
	else:
		#Loop twice so up to two buttons can be pressed simultaneously
		for i in range (0, 8):
			for j in range(0, 8):
				if (switch[i] == True and switch[j] == True):
					#Play sounds corresponding to buttons being pressed
					os.system(sound[i])
					os.system(sound[j])
					time.sleep(0.2)
					#Set buttons to off
					switch[i] =  False
					switch[j] = False
					time.sleep(0.2)					
