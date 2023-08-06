Raspberry Pi Setup
==================
We use a `Raspberry Pi 3 Model B+ <https://www.adafruit.com/product/3055>`_.

Installation
------------
Our instructions assume a Mac is being used.

- Put the micro-SD (e.g.: `cheap one on Amazon <https://www.amazon.com/gp/product/B004ZIENBA/ref=as_li_ss_tl?ie=UTF8&psc=1&linkCode=sl1&tag=bitknittingwo-20&linkId=923f12067ad3395ed04f043c37d8c39f>`_)
  that will hold the Rasp Pi image into an SD Card reader (on our Mac).
- Download a `Rasp Pi image <https://www.raspberrypi.org/downloads/raspbian/>`_.
  `Note: We use the Lite image.`
- Run Etcher to copy the image onto the SD Card.
- Open a terminal window and cd into the boot drive.  For us this was `cd /Volumes/boot`.
- Add "SSH" file to the root of the image.  We do this by opening a terminal on the boot partition and typing `$touch ssh`
- Create the `wpa_supplicant.conf` file::

    $touch wpa_supplicant.conf

Copy the contents into the file::

    $ nano wpa_supplicant.conf


::

    country=US
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1

    network={
        ssid="YOURSSID"
        psk="YOURPWD"
    }


Note: Multiple wifi networks can be set up by following `this example <https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md>`_:
::

    network={
        ssid="SchoolNetworkSSID"
        psk="passwordSchool"
        id_str="school"
    }

    network={
        ssid="HomeNetworkSSID"
        psk="passwordHome"
        id_str="home"
    }

Changing the ssid and psk to match your network.

- 'safely' remove the SD-card.
- Put the SD-card into the Rasp-Pi's micro-SD port
- Power up the Rasp Pi.  Hopefully wireless is working!

We need to know the IP address of the Raspberry Pi on the wireless lan.

- Figure out the wireless lan's subnet::

    ifconfig | grep inet

We find two 192... IP addresses::

    inet 192.168.2.1 netmask 0xffffff00 broadcast 192.168.2.255
    inet 192.168.86.20 netmask 0xffffff00 broadcast 192.168.86.255

The 192.168.2.* is the router's network.  This means the Raspberry Pi is on
192.168.86.*

- Open up Angry IP (or another IP scanning app) and scan for IP addresses in
  the 192.168.86.* network.  We found a new Raspberry Pi with the name raspberrypi.lan.

- start an ssh session by opening a Terminal window, e.g.::

    ssh pi@192.168.86.33

The initial password is raspberry .

Optional - but a **GOOD IDEA** is to change the default password using the::

    $ passwd

command.

- Update the Raspberry Pi's OS::

    sudo apt-get update
    sudo apt-get upgrade
    sudo reboot

- Change the timezone.  The date/time is set to GMT.  We find it easier to work with dates in
  our local timezone.  We used the directions provided by `MBTechWork's website <https://www.mbtechworks.com/how-to/change-time-zone-raspbian.html>`_.
- Install mongodb::

    sudo apt install mongodb
    sudo systemctl enable mongodb

To check if the mongodb service is running::

    systemctl status mongodb

- We use Python's virtual envioronment package::

    sudo apt-get install python3-venv

- We also install git::

    sudo apt-get install git

- Pandas installation was failing with the message::

    Importing the numpy c-extensions failed.

To fix this::

    sudo apt-get install python-dev libatlas-base-dev

That's it for installing Raspberry Pi to communicate with the electricity monitor.

Other Stuff
-----------
Here's some stuff that may or may not be useful.

Mount Drive
~~~~~~~~~~~

There are times when it is useful to access the Rasp Pi drive from the finder.  To do this, we use SSHFS.
- Install `SSHFS <https://osxfuse.github.io/>`_.
- Create a directory to mount to (e.g.: `/users/auser/mount`).
- Open a terminal window and run (replace the raspPi IP address and mount point) e.g.::

    sshfs pi@192.168.86.209: /users/auser/mount

The `/home/pi` directory of the RaspPi will be mounted as a drive in Finder.

Unmount
~~~~~~~

Sometimes the mount gets into a state of limbo.  When that happens, this command seems to work::

    sudo umount -f /users/mj/mount

No SSH, Won't connect to wifi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This happened to us (grrrrrrr)... We had files we wanted to access but could not longer connect to the Rasp Pi over ssh....

We got our Rasp Pi in such a tizzy that we couldn't figure the magic incantations to make
it all better (a warning to us explorers who blindly trust a blog post about ufw.  Luckily we were able to mount the drive on our Mac following
`these directions <https://www.jeffgeerling.com/blog/2017/mount-raspberry-pi-sd-card-on-mac-read-only-osxfuse-and-ext4fuse>`_::

    sudo mkdir /Volumes/rpi
    brew cask install osxfuse
    brew install ext4fuse
    diskutil list

Now here is where it gets a tad tricky figuring out what partition ID we want to mount.::

    /dev/disk3 (internal, physical):
    #:                       TYPE NAME                    SIZE       IDENTIFIER
    0:     FDisk_partition_scheme                        *63.9 GB    disk3
    1:             Windows_FAT_32 boot                    268.4 MB   disk3s1
    2:                      Linux                         63.6 GB    disk3s2

Our SD Card reader is internal.  We want the Linux partition.  So the ID is
`disk3s2`::

    sudo ext4fuse /dev/disk3s2 /Volumes/rpi -o allow_other

now we can access the file from Terminal.

At least we can get the files off the SD card!






