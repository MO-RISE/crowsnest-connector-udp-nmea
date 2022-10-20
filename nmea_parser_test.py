from cmath import e
import pynmea2


mbytes = b"UdPbC\x00\\s:GN9999,n:210*0B\\$GNGSA,M,1,04,06,07,09,11,16,20,,,,,,1.53,1.09,1.07,1*0F\r\n\\s:GN9999,n:211*0A\\$GNGSA,M,1,65,74,75,88,,,,,,,,,1.53,1.09,1.07,2*07\r\n\\s:GN9999,n:212*09\\$GNGSA,M,1,303,308,313,,,,,,,,,,1.53,1.09,1.07,3*3E\r\n\\s:GN9999,n:213*08\\$GNGSA,M,1,414,,,,,,,,,,,,1.53,1.09,1.07,4*32\r\n\\s:GN9999,n:214*0F\\$GNGGA,114835.60,5742.5522736,N,01156.8392494,E,5,15,1.1,5.18,M,35.78,M,,*77\r\n\\s:GN9999,n:215*0E\\$GNVTG,,T,,M,,N,,K,A*3D\r\n\\s:GN9999,n:216*0D\\$PASHR,114835.60,027.23,T,-75.83,,,3.158,,4.831,1,*22\r\n\\s:GN9999,n:217*0C\\$GNRMC,114835.60,A,5742.5522736,N,01156.8392494,E,,,191022,,W,D,V*61\r\n\\s:GN9999,n:218*03\\$GNZDA,114835.60,19,10,2022,,*7F\r\n\\s:GN9999,n:219*02\\$GNGST,114835.60,,,,,0.264,0.170,0.334*47\r\n\\s:GN9999,n:221*09\\$GNTHS,27.23,V*3A\r\n\\s:GN9999,n:220*08\\$GNROT,0.0,V*38\r\n"

mbytes = b"UdPbC\u0000\\s:GN9999,n:571*0B\\$GNGSA,M,1,01,03,21,32,,,,,,,,,1.89,1.31,1.37,1*09\r\n\\s:GN9999,n:572*08\\$GNGSA,M,1,85,87,,,,,,,,,,,1.89,1.31,1.37,2*08\r\n\\s:GN9999,n:573*09\\$GNGSA,M,1,312,319,,,,,,,,,,,1.89,1.31,1.37,3*00\r\n\\s:GN9999,n:574*0E\\$GNGSA,M,1,419,420,422,,,,,,,,,,1.89,1.31,1.37,4*32\r\n\\s:GN9999,n:575*0F\\$GNGGA,070559.61,5742.5507032,N,01156.8375806,E,5,11,1.3,1.74,M,35.78,M,,*70\r\n\\s:GN9999,n:576*0C\\$GNVTG,166.99,T,166.99,M,0.11,N,0.20,K,D*3A\r\n\\s:GN9999,n:577*0D\\$PASHR,070559.61,319.50,T,-37.37,,,0.853,,2.234,1,*2C\r\n\\s:GN9999,n:578*02\\$GNRMC,070559.61,A,5742.5507032,N,01156.8375806,E,0.11,166.99,201022,,W,D,V*65\r\n\\s:GN9999,n:579*03\\$GNZDA,070559.61,20,10,2022,,*70\r\n\\s:GN9999,n:580*05\\$GNGST,070559.61,,,,,0.109,0.133,0.212*48\r\n\\s:GN9999,n:581*04\\$GNROT,0.0,V*38\r\n\\s:GN9999,n:582*07\\$GNTHS,319.50,V*00\r\n"


nmea_parameters = {
    "timestamp": None,
    "datestamp": None,
    "lat": None,
    "lat_dir": None,
    "lon": None,
    "lon_dir": None,
    "sog": None,
    "cog": None,
    "rot": None,
    "roll": None,
    "heading": None,
    "heading_accuracy": None,
    "altitude": None,
    "gps_quality": None,
    "num_satellites": None,
}

# print(nmea_msg["message"])
nm = mbytes.decode("utf-8")
nmea__list = nm.split("\r")

# print(nmea__list)

for nmea_str in nmea__list:
    nmea_str = "$" + nmea_str.split("$")[-1]

    try:
        nmea_type_msg = nmea_str.split(",")[0].replace("$", "")
     
        if nmea_type_msg == "PASHR":
            PASHR_items = nmea_str.split(",")
            PASHR = {
                "heading": float(PASHR_items[2]),
                "roll": float(PASHR_items[4]),
                "pitch": PASHR_items[5],
                "roll_accuracy": PASHR_items[7],
                "heading_accuracy": PASHR_items[9],
            }
            nmea_parameters.update(PASHR)

        msg = pynmea2.parse(nmea_str)

        if msg.sentence_type == "GGA":
            GGA = {
                "timestamp": msg.timestamp.isoformat(),
                 "lon": float(msg.lon)  /100,
                "lon_dir": msg.lon_dir,
                "lat": float(msg.lat) /100,
                "lat_dir": msg.lat_dir,
                "altitude": msg.altitude,
                "lat_dir": msg.lat_dir,
                "num_satellites": msg.num_sats,
                "gps_quality": msg.gps_qual,
            }
            nmea_parameters.update(GGA)

        elif msg.sentence_type == "RMC":
            RMC = {
                "datestamp": msg.datestamp.isoformat(),
            }
            nmea_parameters.update(RMC)

        elif msg.sentence_type == "VTG":
            VTG = {
                "sog": msg.spd_over_grnd_kts,
                "cog": msg.true_track,
            }
            nmea_parameters.update(VTG)

        elif msg.sentence_type == "ROT":
            ROT = {
                "rot": msg.rate_of_turn,
            }
            nmea_parameters.update(ROT)

        elif msg.sentence_type == "GST":
            GST = {
                "std_dev_altitude": msg.std_dev_altitude,
                "std_dev_longitude": msg.std_dev_longitude,
                "std_dev_latitude": msg.std_dev_latitude,
            }
            nmea_parameters.update(GST)

    except Exception as e:
        print(e)
        pass


print("FINAL:", nmea_parameters)
