# Author:
#  Romain Bentz (pixis - @hackanddo)
# Website:
#  https://beta.hackndo.com

"""
# RENAME THIS FILE TO tests_config.py
"""

# IP address where LSASS can be dumped
ip_address = "192.168.56.201"

# IP address where LSASS is protected (empty to skip tests)
ip_address_protected = ""

# Domain Name
domain = "adsec.local"

# User with admin rights on ip_address and ip_address_protected
da_login = "jsnow"
da_password = "Winter_is_coming_!"

# User without admin rights on ip_address (empty to skip tests)
usr_login = "jlannister"
usr_password = "summer4ever!"

# Local tools for dumping methods (empty to skip tests)
procdump_path = "/home/pixis/Tools/Windows/Sysinternals/procdump.exe"
dumpert_path = "/home/pixis/Tools/Windows/Dumpert/Outflank-Dumpert.exe"
