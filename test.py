lat = 1156.8426456

lat_deg = lat / 100  # to degrees

lat_deg_min = ((lat_deg % 1)*100) /60

print("Deg:", int(lat_deg) +  lat_deg_min )
print("Deg_MIN:", lat_deg_min )