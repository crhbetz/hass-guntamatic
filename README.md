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
