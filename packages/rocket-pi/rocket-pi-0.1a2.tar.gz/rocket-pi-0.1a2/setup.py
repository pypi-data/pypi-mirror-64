# +---------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control key enabling technology (Rocket)
#      
#      Target:     ARMV61A
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +---------------------------------------------------------------------------+

import atexit
import os
import sys
from setuptools import setup
from setuptools.command.install import install

with open("README.md", "r") as fh:
    long_description = fh.read()

def logo():
    print()
    print("                                          ")
    print("######                                    ")
    print("#     #  ####   ####  #    # ###### ##### ")
    print("#     # #    # #    # #   #  #        #   ")
    print("######  #    # #      ####   #####    #   ")
    print("#   #   #    # #      #  #   #        #   ")
    print("#    #  #    # #    # #   #  #        #   ")
    print("#     #  ####   ####  #    # ######   #   ")
    print("                                          ")


class CustomInstall(install):
    def run(self):
        def _post_install():

            # Add your post install code here
            logo()
            import rocket
            print(rocket.joke())
            import rocketlauncher
            print(rocketlauncher.joke())
            # Get hostapd or dnsmasq if needed
            get_hostapd()
            get_dnsmasq()
            get_webiopi()


        atexit.register(_post_install)
        install.run(self)
        

setup(name='rocket-pi',
      version='0.1a2',
      description='Remote open control key enabling technology (Rocket)',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/gulliversoft/rocket',
      author='gulliversoft',
      author_email='fg7@gulliversoft.com',
      license='GPL3',
      packages=['rocket','rocketlauncher'],
      zip_safe=False,
      classifiers=["Intended Audience :: Education", "Operating System :: POSIX :: Linux"],
      cmdclass={'install': CustomInstall})
      #install_requires[''])

def get_webiopi():
    """
    Try to install webiopi on host machine if not present

    :return: None
    :rtype: None
    """
    
    if not os.path.isfile("/home/pi/rocket/WebIOPi-0.7.1"):
        print("WebIOPi not found in /home/pi/rocket/WebIOPi-0.7.1, install now? [y/n]")
        os.system("tar xvzf WebIOPi-0.7.1.bin")
        
    os.system("cd WebIOPi-0.7.1")
    os.system("./setup.sh")
        
    

def get_dnsmasq():
    """
    Try to install dnsmasq on host machine if not present

    :return: None
    :rtype: None
    """

    if not os.path.isfile("/etc/dnsmasq.conf"):
        print("dnsmasq not found in /usr/sbin/dnsmasq, install now? [y/n] ")
        os.system("apt-get install dnsmasq")
    
    if not os.path.isfile("/usr/sbin/dnsmasq"):
        sys.exit(("\nUnable to install the \'dnsmasq\' package!\n" + 
                  "This process requires a persistent internet connection!\n" +
                  "Run apt-get update for changes to take effect.\n" +
                  "Rerun the script to install dnsmasq.\n" +
                  "Closing"))


def get_hostapd():
    """
    Try to install hostapd on host system if not present

    :return: None
    :rtype: None
    """

    if not os.path.isfile("/usr/sbin/hostapd"):
        print("hostapd not found in /usr/sbin/hostapd, install now? [y/n]")
        os.system("apt-get install hostapd")

    if not os.path.isfile("/usr/sbin/hostapd"):
        sys.exit(("\nUnable to install the \'hostapd\' package!\n" + 
        "This process requires a persistent internet connection!\n" +
        "Run apt-get update for changes to take effect.\n" +
        "Rerun the script to install hostapd.\n" +
        "Closing"))
        
        

