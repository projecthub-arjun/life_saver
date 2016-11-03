import googlemaps

#Function to use google reverse lookup
def reverse_gps_lookup(lat, long):
    try:
        gmaps = googlemaps.Client(key='AIzaSyBMiCLiRo2vjKWsu4Tsc9W4U2wOKv_ODRk')
        reverse_geocode_result = gmaps.reverse_geocode((lat, long))
        return reverse_geocode_result[0]['formatted_address']
    except:
        return ''
print reverse_gps_lookup('8.501877','76.935268') 