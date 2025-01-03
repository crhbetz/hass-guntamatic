# Guntamatic

Home Assistant Custom Component for Guntamatic Biostar furnaces.

# Scope of the project

This software has been developed to read out data from the Guntamatic Biostar furnace that came with our house:

* Type: Biostar 15kW
* installed: circa 2012
* Software: 3.2d

For every metric available, a suitable sensor with the correct unit of measurement should be created after setup.

In principle, any Guntamatic furnace that is connected to the local network and exposes `/daqdesc.cgi` and `/daqdata.cgi` _should_ be supported. I don't know what range of hardware / software by Guntamatic that might be.

I am aware there seem to be options to gain further access by obtaining access tokens / passwords from Guntamatic. I currently have no plans to add any form of deeper access options to this component. That is because of a lack of time and personal use-case.

Anyone intending to add new functions, new devices with different interfaces etc. is strongly encouraged to fork this repository.

# Setup

## HACS

I recommend using [HACS](https://hacs.xyz/) for installation.

1. Open HACS, click the three dots in the upper right corner, select "custom repositories".
2. Add this repository (https://github.com/crhbetz/hass-guntamatic) as type "integration".
3. Find the integration in HACS and install it.
4. Follow the instructions of HACS. It might report a required restart.
5. Go to "Configuration", "Integrations", click "+" and find "Guntamatic".
6. Add a new entry:
    * `Host`: usually the IP address of the Guntamatic device (if anything else, you'll know yourself)
    * `Name`: whatever you want this particular device to be called - it'll be part of entity ids like `sensor.<name>_leistung`
    * `scan_interval`: every n seconds HA will query data from the device

## Manual

Either you know how, or you better use HACS :-)
