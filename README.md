# ImageRite
Python program to write Raspberry pi OS  to a USB drive or sd card.

The inspiration and credit for the idea of this program comes from the Raspberry Pi foundation; under the heading of Installations, the process of writing an image to an sd card or USB device is given.  As I had only raspbian to work with, i had to use the built in dd command. After many repetitive image writings and so on, I decided to write this program to automate this process. It also provides for the optional use of SFTP to retrieve the image or zip OS files. The program can write image or compressed zip files to the USB or sd card device, as stated in the raspberry pi Installation section. This program is provided under the Apache 2.0 license and is provided AS-IS without any express warranties or expectations. I am not an experienced python programmer, as this is my first project. 

In summary, the program can: SFTP a remote file, or skip directly to writing an image to a USB or sd card. It has provisions for checking the written file via truncate and diff; will flush the write cache after checking the file and unmount and eject the USB or sd card for safe removal.

If you notice, there is another file, buos.py which will do the same function of the ImageRite, but without the SFTP, or error checking of the written media. Use either one you wish, however, this program is provided under the Apache 2.0 license and is provided AS-IS without any express warranties or expectations.
