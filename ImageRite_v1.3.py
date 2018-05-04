#!/usr/bin/python3
#
#
# This version supports image sftp from a remote server on the network,
# image checking, automatic unmounting and ejection.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Status of this version is 'IN testing'
# 
# Update: ImageRite_v1.3.py
#    
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# This release corrects an issue with python variable space, as suggested
# by Pi forum user KLL. It also utilizes Command Line Arguments.
# Usage syntax for this program:
#
#   ImageRite_v1.3.py -i <inputfile> -o <outputfile>
#
#  Improvements in this version is automatic checking for USB or sd card
#  insertion. Program stops if not inserted. enhanced file typ checking
#  to insure only an image or zip file is written. Other extensions are
#  rejected!
#
#  The plan is that I will eventually replace the os.sytem commands with
#  subprocess commands.
#
# Copyright 2018 Kelly Mabry
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# import the os for commands from OS/usr/bin/python3
#
import os, sys, getopt, time, subprocess

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('test.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print ('Input file is ', inputfile)
   print ('Output file is ', outputfile)
   print()
# Automatically tests for the existance of a USB drive or sd card here. rv3 =1, not mounted
# otherwise, contine. Much leaner and safer this way...
   rv3 = subprocess.call("mountpoint -q /mnt/usbdrive", shell=True)
   if rv3 == 1:
      sys.exit("USB drive or sd card NOT MOUNTED!  Exiting program...")
   else:
      cwd = os.getcwd()   # get the current working directory
      #  Testing not just img and zip, but iso file, too. Expand strip to test for
      #  3 characters; img, zip and osi; the last being invalid for Rpi's!
      filtyp = inputfile[-3:-1]
      print(filtyp)
      #
      print("Welcome to the ImageRite program. You will now write an OS to a USB or sdcard... ")
      print("WARNING! This program writes to the external sdcard or USB on /dev/sdX ")
      print("***** WARNING!***** This action will erase all files on the device!! ")
      print()
      if filtyp == 'im':   # img file; testing 2 characters to determine file type
         print()
         str = "sudo dd bs=4M if="+inputfile+" of="+outputfile+" status=progress conv=fsync"
         print()
         print("Writing image to device "+outputfile)
         print()
         os.system (str)
      elif filtyp == 'zi':  # zip file; testing 2 characters to determine file type
         print()
         str = "unzip -p "+inputfile+ "| sudo dd bs=4M of= "+outputfile+" status=progress conv=fsync"
         print("Unzipping and writing "+inputfile+" to "+outputfile)
         print()
         str = "sudo dd bs=4M if="+inputfile+" of="+outputfile+" status=progress conv=fsync"
         os.system (str)
         print()
      elif filtyp == 'is':  # iso file; testing 2 characters to determine file type 
         print()
         str = "sudo dd bs=4M if="+inputfile+" of="+outputfile+" status=progress conv=fsync"
         print()
         print("Writing .iso image to device "+outputfile)
         print()
         os.system (str)
      else:
         sys.exit("Invalid file type! Exiting program...")
# If not either an im(g) or zi(p) file, then abort the write and exit
# Note: I could test for an is(o) file, and add a write feature here tbd.
# thinking about doing iso file write section for the raspbian iso for
# non - arm operating systems; specifically usb drives to install stretch
# for Raspberry Pi Desktop (for PC and Mac)        
#
# 
# set up for flushing write cache, unmounting and ejecting devices...
      print()
      print("copying image to test into "+cwd+"/from-sd-card.img")
      print()
      cpim = "sudo dd bs=4M if="+outputfile+" of=from-sd-card.img status=progress"
      os.system (cpim)    
      print()
      print("truncating image...")
      print()
      trunc = "sudo truncate --reference "+inputfile+" "+cwd+"/from-sd-card.img"
#sudo truncate --reference /home/pi/test_os.img from-sd-card.img
      os.system (trunc)
      print("checking image for differences...")
      print()
#sudo diff -s /home/pi/test_os.img /home/pi/from-sd-card.img
      dif = "sudo diff -s "+inputfile+" "+cwd+"/from-sd-card.img"
      os.system (dif)
# remove the /home/pi/from-sd-card.img
      print("removing the file"+cwd+"/from-sd-card.img...")
      print()
      rmfil = "rm "+cwd+"/from-sd-card.img"
      os.system(rmfil)
# flush the write cache and proceed with drive unmount and eject.    
      os.system ('sync')
      print()
      driveumount = "sudo umount "+outputfile
      driveject = "sudo eject "+outputfile  
      os.system (driveumount)
      os.system (driveject)
      print("Target drive "+outputfile+" unmounted and ejected!")
      print()
      print("You are done, please REMOVE your drive!")
 
   
if __name__ == "__main__":
   main(sys.argv[1:])




