from cmath import e
import pynmea2


mbytes = b'UdPbC\x00\\s:GN9999,n:210*0B\\$GNGSA,M,1,04,06,07,09,11,16,20,,,,,,1.53,1.09,1.07,1*0F\r\n\\s:GN9999,n:211*0A\\$GNGSA,M,1,65,74,75,88,,,,,,,,,1.53,1.09,1.07,2*07\r\n\\s:GN9999,n:212*09\\$GNGSA,M,1,303,308,313,,,,,,,,,,1.53,1.09,1.07,3*3E\r\n\\s:GN9999,n:213*08\\$GNGSA,M,1,414,,,,,,,,,,,,1.53,1.09,1.07,4*32\r\n\\s:GN9999,n:214*0F\\$GNGGA,114835.60,5742.5522736,N,01156.8392494,E,5,15,1.1,5.18,M,35.78,M,,*77\r\n\\s:GN9999,n:215*0E\\$GNVTG,,T,,M,,N,,K,A*3D\r\n\\s:GN9999,n:216*0D\\$PASHR,114835.60,027.23,T,-75.83,,,3.158,,4.831,1,*22\r\n\\s:GN9999,n:217*0C\\$GNRMC,114835.60,A,5742.5522736,N,01156.8392494,E,,,191022,,W,D,V*61\r\n\\s:GN9999,n:218*03\\$GNZDA,114835.60,19,10,2022,,*7F\r\n\\s:GN9999,n:219*02\\$GNGST,114835.60,,,,,0.264,0.170,0.334*47\r\n\\s:GN9999,n:220*08\\$GNROT,0.0,V*38\r\n\\s:GN9999,n:221*09\\$GNTHS,27.23,V*3A\r\n'

# print(nmea_msg["message"])
nm =  mbytes.decode("utf-8") 
print(type(nm))
nmea__list = nm.split("\r")

# print(nmea__list)

for nmea_str  in nmea__list:
    nmea_str =  "$"+ nmea_str.split("$")[-1]
    print(nmea_str)
    try:
        msg = pynmea2.parse( nmea_str)
        print(repr(msg))
        print("--------")
    except Exception as e:
        print(e)
    