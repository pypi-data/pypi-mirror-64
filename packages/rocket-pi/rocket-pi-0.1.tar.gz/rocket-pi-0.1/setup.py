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
            def find_module_path():
                for p in sys.path:
                    if os.path.isdir(p) and my_name in os.listdir(p):
                        return os.path.join(p, my_name)
            install_path = find_module_path()

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
      version='0.1',
      description='Remote open control key enabling technology (Rocket)',
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
        install = raw_input(("[" + constants.T + "*" + constants.W + "] WebIOPi not found " +
                             "in /home/pi/rocket/WebIOPi-0.7.1, " + "install now? [y/n] "))
        
        if install == "y":
            os.system("tar xvzf WebIOPi-0.7.1.bin")
        else:
            sys.exit(("[" + constants.R + "-" + constants.W + "] WebIOPi " +
                      "not found"))
            
    if not os.path.isfile("/home/pi/rocket/WebIOPi-0.7.1"):
        hostapd_message = ("\n[" + constants.R + "-" + constants.W + "] Unable to install the " +
                           "\'WebIOPi\' from archive!\nClosing")
        sys.exit(hostapd_message)
        
    os.system("cd WebIOPi-0.7.1")
    os.system("./setup.sh")
        
    

def get_dnsmasq():
    """
    Try to install dnsmasq on host machine if not present

    :return: None
    :rtype: None
    """

    if not os.path.isfile("/etc/dnsmasq.conf"):
        install = raw_input(("[" + constants.T + "*" + constants.W + "] dnsmasq not found " +
                             "in /usr/sbin/dnsmasq, " + "install now? [y/n] "))

        if install == "y":
            os.system("apt-get -y install dnsmasq")
        else:
            sys.exit(("[" + constants.R + "-" + constants.W + "] dnsmasq " +
                      "not found in /usr/sbin/dnsmasq"))
    
    if not os.path.isfile("/usr/sbin/dnsmasq"):
        hostapd_message = ("\n[" + constants.R + "-" + constants.W + "] Unable to install the " +
                           "\'dnsmasq\' package!\n[" + constants.T + "*" + constants.W + "] " +
                           "This process requires a persistent internet connection!\n" +
                           "Run apt-get update for changes to take effect.\n[" + constants.G +
                           "+" + constants.W + "] Rerun the script to install dnsmasq.\n[" +
                           constants.R + "!" + constants.W + "] Closing")
        sys.exit(hostapd_message)


def get_hostapd():
    """
    Try to install hostapd on host system if not present

    :return: None
    :rtype: None
    """

    if not os.path.isfile("/usr/sbin/hostapd"):
        install = raw_input(("[" + constants.T + "*" + constants.W + "] hostapd not found in " +
                             "/usr/sbin/hostapd, install now? [y/n] "))

        if install == "y":
            os.system("apt-get -y install hostapd")
        else:
            sys.exit(("[" + constants.R + "-" + constants.W + "] hostapd not found in " +
                      "/usr/sbin/hostapd"))

    if not os.path.isfile("/usr/sbin/hostapd"):
        hostapd_message = ("\n[" + constants.R + "-" + constants.W + "] Unable to install the " +
                           "\'hostapd\' package!\n[" + constants.T + "*" + constants.W + "] " +
                           "This process requires a persistent internet connection!\n" +
                           "Run apt-get update for changes to take effect.\n[" + constants.G +
                           "+" + constants.W + "] Rerun the script to install hostapd.\n[" +
                           constants.R + "!" + constants.W + "] Closing")
        sys.exit(hostapd_message)
        
        

