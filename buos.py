#!/usr/bin/env python
#
# Copyright 2018 Kelly Mabry
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
# *****NOTICE*****
# This was the original concept program thought of as back up OS, or buos.py
# the program does not support sftp, or checking of the written images. it is 
# just the core writing to the sd card or USB device.
# *****NOTICE*****
# 
#import the os for commands from OS
import os
#
#
# initialize variables at start.
# 
driveject = ""
filtyp = ""     # filtyp will be either "i" or "z"
sda_test = ""   # sda_test determines if the sd card or USB device is present.
sdX = ""        # sdX is the "/dev/sda or /dev/sdb device chosen by human input
IMG = "i"       # This is the test variable compared with filtyp to choose which function to run.
ZIP = "z"       # This is the test variable compared with filtyp to choose which function to run.
N = "n"         # This is the variable which stores the No or n answer if the sd card is not present.
Y = "y"         # This is the variable which stores the Yes or y answer if the sd card is present.
#
#
#
# Set up functions to be used in the program.
#
#
# set up functions for flushing write cache, unmounting and ejecting devices...
#
def fin(sdX):
    print("")
    driveumount = "sudo umount /dev/"+sdX
    driveject = "sudo eject /dev/"+sdX  
    os.system (driveumount)
    os.system (driveject)
    print("Target drive /dev/"+sdX+" unmounted and ejected!")
    print("")
    print("Congratulations you are done!, please REMOVE your drive!!")
    return
#
# set up functions for each method of writing to USB or sd card...
#
def ozip(filtyp, sdX):
    pathname = (input("Enter path and filename to be written..ZIP file only! "))
    print("")
    str = "unzip -p "+pathname+ "| sudo dd bs=4M of=/dev/"+sdX+" status=progress conv=fsync"
    print("Unzipping and writing image to device /dev/"+sdX)
    os.system (str)
    fin(sdX)
    return
#
#
#   
def oimg(filtyp, sdX):
    pathname = (input("Enter path and filename to be written..IMG file only!! "))
    str = "sudo dd bs=4M if="+pathname+" of=/dev/"+sdX+" status=progress conv=fsync"
    print("")
    print("Writing image to device /dev/"+sdX)
    os.system (str)
    fin(sdX)
    return
#
# program main body starts here.
#
# clear terminal screen
os.system ('clear')
print("")
print("Welcome to the ImageRite program. You will write an OS to a USB or sdcard... ")
print("WARNING! This program writes to the external sdcard or USB on /dev/sdX ")
print("***** WARNING!***** This action will erase all files on the device!! ")
print("")
os.system ('lsblk')
print("")
sda_test = (input("Input y if the /dev/sdX card is present, n if not present!: "))
#
print("")
if (sda_test == Y):
        sdX = (input("Input the drivename; where sdX = sda or sdb,etc../dev/"))
        print("")
        filtyp = (input("Input whether an IMG [i] or a ZIP [z] is to be written: "))
        if filtyp == IMG:
            oimg(filtyp, sdX)   # run oimg function; passing filtyp = IMG, sdX
        elif filtyp == ZIP:
            ozip(filtyp, sdX)   # run ozip function; passing filtyp = ZIP, sdX
        else:
            print("WARNING!! INVALID ENTRY!!")
# 
#       
else:
    if (sda_test == N):
            print("WARNING!! sd card not present!!")
    else:
            print("WARNING!! INVALID ENTRY!!")


