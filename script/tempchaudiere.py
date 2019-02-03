import os
import glob
import time
import sys


base_dir = '/home/pi/pidomo/chaudiere'
cmd = base_dir + '/sendCommand 6 777 10 temp >/dev/null'
os.system(cmd)
cmd = base_dir + '/tempReception 1 5'
fin, fout = os.popen4(cmd)
#print fout.read() #standard out



def read_temp_raw():
    lines = fout.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    #print(lines[0])
    equals_pos = lines[0].find('t=')
    if equals_pos != -1:
        temp_string = lines[0][equals_pos+2:]
        temp_c = float(temp_string) / 100.0
        temp_c = round(temp_c,1)
        return temp_c
	

print(read_temp())	
