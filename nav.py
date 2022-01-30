import requests
import json


class driving_distance:

    def dist(start, end):
        url = "http://www.mapquestapi.com/directions/v2/route?key=obKnWOA9Aklsxgy8OpA54sjSY7W0YO58&from=" + start + "&to=" + end
        payload={}
        headers = {
        'Cookie': 'JSESSIONID=D2DAB2375BBD5635E8A0E88280D8FDCB'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        resp = response.json()
        return resp['route']['distance']

    
