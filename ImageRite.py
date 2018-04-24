#!/usr/bin/env python
#
# ImageRite
# version 1.2
#
# This version supports image sftp from a remote server on the network,
# image checking, automatic unmounting and ejection.
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
#
#import the os for commands from OS
import os
#
# initialize variables at start.
# 
sftp_test = ""
rmfil = ""
cwd = ""
pathname = ""
cpim = ""
trunc = ""
dif = ""
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
# set up a function to retrieve an OS img or zip via sftp;
def sftpfil():
    print("Welcome to the ImageRite program.  You may request an .img or .zip file")
    print("via sftp from a server on the network...")
    print()
    sftp_test = (input("Input [y] if the remote file is desired, [n] if not desired!: "))
    print()
    if (sftp_test == "y"):
        os.system('clear')
        os.system('arp')
        print()
        addr = (input("Input the IP address of the remote server: "))
        print()
        sftp = "sftp "+addr
        os.system(sftp)
    else:
        print("Proceeding to ImageRite...")
        return
#
# set up functions for flushing write cache, unmounting and ejecting devices...
def cln(filtyp, pathname, cwd, sdX):
    print()
    print("copying image to test into "+cwd+"/from-sd-card.img")
    print()
    cpim = "sudo dd bs=4M if=/dev/"+sdX+" of=from-sd-card.img status=progress"
    os.system (cpim)    
    print()
    print("truncating image...")
    print()
    trunc = "sudo truncate --reference "+pathname+" "+cwd+"/from-sd-card.img"
#sudo truncate --reference /home/pi/test_os.img from-sd-card.img
    os.system (trunc)
    print("checking image for differences...")
    print()
#sudo diff -s /home/pi/test_os.img /home/pi/from-sd-card.img
    dif = "sudo diff -s "+pathname+" "+cwd+"/from-sd-card.img"
    os.system (dif)
# remove the /home/pi/from-sd-card.img
    print("removing the file"+cwd+"/from-sd-card.img...")
    print()
    rmfil = "rm "+cwd+"/from-sd-card.img"
    os.system(rmfil)
# flush the write cache and proceed with drive unmount and eject.    
    os.system ('sync')
    print()
    driveumount = "sudo umount /dev/"+sdX
    driveject = "sudo eject /dev/"+sdX  
    os.system (driveumount)
    os.system (driveject)
    print("Target drive /dev/"+sdX+" unmounted and ejected!")
    print()
    print("You are done, please REMOVE your drive!")    
    return filtyp, pathname, cwd, sdX
#
# set up functions for each method of writing to USB or sd card...
def ozip(filtyp, pathname, cwd, sdX):
    str = "unzip -p "+pathname+ "| sudo dd bs=4M of=/dev/"+sdX+" status=progress conv=fsync"
    print()
    print("Unzipping and writing image to device /dev/"+sdX)
    print()
    os.system (str)
    return filtyp, pathname, cwd, sdX
#   
def oimg(filtyp, pathname, cwd, sdX):
    str = "sudo dd bs=4M if="+pathname+" of=/dev/"+sdX+" status=progress conv=fsync"
    print()
    print("Writing image to device /dev/"+sdX)
    print()
    os.system (str)
    return filtyp, pathname, cwd, sdX

# program main body starts here.
#
def main(filtyp, pathname, cwd, sdX): 
    os.system ('clear')     # clear terminal screen
    cwd = os.getcwd()       # get the current working directory
    sftpfil()               # function to retrieve img or zip from remote server
    os.system ('clear')     # clear terminal screen
    print("Welcome to the ImageRite program. You will now write an OS to a USB or sdcard... ")
    print("WARNING! This program writes to the external sdcard or USB on /dev/sdX ")
    print("***** WARNING!***** This action will erase all files on the device!! ")
    print()
    os.system ('lsblk')
    print()
    sda_test = (input("Input y if the /dev/sdX device is present, n if not present!: "))
#
    print()
    if (sda_test == Y):
            sdX = (input("Input the drivename; where sdX = sda or sdb,etc../dev/"))
            print()
            filtyp = (input("Input whether an IMG [i] or a ZIP [z] is to be written: "))
            if filtyp == IMG:
                pathname = (input("Enter path and filename to be written..IMG file only!! "))
                oimg(filtyp, pathname, cwd, sdX)   # run oimg function; passing filtyp = IMG, sdX
                cln(filtyp, pathname, cwd, sdX)
            elif filtyp == ZIP:
                pathname = (input("Enter path and filename to be written..ZIP file only! "))
                ozip(filtyp, pathname, cwd, sdX)   # run ozip function; passing filtyp = ZIP, sdX
                cln(filtyp, pathname, cwd, sdX)
            else:
                print("WARNING!! INVALID ENTRY!!")
# 
#       
    else:
        if (sda_test == N):
                print("WARNING!! USB device or sd card not present!!")
        else:
                print("WARNING!! INVALID ENTRY!!")


# Execute main() function
if __name__ == '__main__':
    main(filtyp, pathname, cwd, sdX)
