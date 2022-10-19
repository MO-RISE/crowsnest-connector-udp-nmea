from cmath import e
import pynmea2


nmea_msg = {
    "sent_at": "2022-10-19T10:33:33.572157+00:00",
    "message": "UdPbC\u0000\\s:GN9999,n:46*3A\\$GNGSA,M,1,04,,,,,,,,,,,,2.51,1.69,1.85,1*0F\r\n\\s:GN9999,n:47*3B\\$GNGSA,M,1,71,72,,,,,,,,,,,2.51,1.69,1.85,2*0B\r\n\\s:GN9999,n:48*34\\$GNGSA,M,1,303,305,315,334,,,,,,,,,2.51,1.69,1.85,3*0C\r\n\\s:GN9999,n:49*35\\$GNGSA,M,1,414,428,,,,,,,,,,,2.51,1.69,1.85,4*01\r\n\\s:GN9999,n:50*3D\\$GNGGA,103428.21,5742.5520041,N,01156.8401531,E,5,09,1.7,6.53,M,35.78,M,,*75\r\n\\s:GN9999,n:51*3C\\$GNVTG,039.52,T,039.52,M,0.35,N,0.64,K,D*3C\r\n\\s:GN9999,n:52*3F\\$PASHR,103428.21,337.80,T,-71.71,,,3.437,,5.178,1,*2A\r\n\\s:GN9999,n:53*3E\\$GNRMC,103428.21,A,5742.5520041,N,01156.8401531,E,0.35,39.52,191022,,W,D,V*5F\r\n\\s:GN9999,n:54*39\\$GNZDA,103428.21,19,10,2022,,*7C\r\n\\s:GN9999,n:55*38\\$GNGST,103428.21,,,,,0.536,0.611,0.889*49\r\n\\s:GN9999,n:56*3B\\$GNROT,0.0,V*38\r\n\\s:GN9999,n:57*3A\\$GNTHS,337.80,V*01\r\n",
}

# print(nmea_msg["message"])
nmea__list = nmea_msg["message"].split("\r")

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
        continue