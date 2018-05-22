#!/usr/bin/python3
#
#to insure only an image or zip file is written.
# Thiis version supports
# image checking, automatic unmounting and ejection.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Status of this version is 'Ready for Release'
# 
# Update: ImageRite_v1.5.py
#    
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#  This release corrects an issue with python variable space, as suggested
#  by Pi forum user KLL. It also utilizes Command Line Arguments.
#  Usage syntax for this program:
#
#   ImageRite_v1.5.py -i <inputfile> -o <outputfile>
#
#  Enhanced file type checking to insure only an image or zip file is written.
#  Other extensions are rejected!
#  UPDATE! V1.5 now will write an .iso file to sd card or USB device!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  Reorganized code for efficiency. Currently no image checking
#  performed on .zip or .iso files, only on image (.img) files.
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#  I will eventually replace the os.sytem commands with
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
# Automatically tests for the existance of a USB drive or sd card here. rv3 == 1, the drive is
# not mounted; otherwise, continue. Much leaner and safer this way...
# This is not working as it was initially. Also, there needs to be a way to block writing to the
# system drive so that it will not write to the computer's drive, ususally /dev/sda.
#  subprocess.call('ls /dev/sdb', shell=True)
   cwd = os.getcwd()   # get the current working directory
#  Testing not just img and zip, but iso file, too. Expand strip to test for
#  3 characters; img, zip and iso.
   filtyp = inputfile[-3:-1]    # checks for im = img; zi = zip; and is = iso
#  print(filtyp)
#
   print("Welcome to the ImageRite program. You will now write an OS to a USB or sdcard... ")
   print("WARNING! This program writes to the external sdcard or USB on "+outputfile)
   print("***** WARNING!***** This action will erase all files on the device!! ")
   print()
   if filtyp == 'im':   # img file; testing 2 characters to determine file type
      str = "sudo dd bs=4M if="+inputfile+" of="+outputfile+" status=progress conv=fsync"
      print("Writing image to device "+outputfile)
      print()
      os.system (str)
      # 
# set up for copying image to from-sd-card.img
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
   elif filtyp == 'zi':  # zip file; testing 2 characters to determine file type
      #print('filetype is ', filtyp)
      print()
      str = "unzip -p "+inputfile+ "| sudo dd bs=4M of= "+outputfile+" status=progress conv=fsync"
      print("Unzipping and writing "+inputfile+" to "+outputfile)
      print()
      os.system(str)
   elif filtyp == 'is':  # iso file; testing 2 characters to determine file type 
      #print('filetype is ', filtyp)
      #print()
      str = "sudo dd bs=4M if="+inputfile+" of="+outputfile+" status=progress conv=fsync"
      print()
      print("Writing .iso image to device "+outputfile)
      print()
      os.system (str)
   else:
      sys.exit("Invalid file type! Exiting program...")
# If not either an im(g), zi(p) or .is(o) file, then abort the write and exit
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




