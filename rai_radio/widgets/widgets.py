from typing import List
import requests
import json
import os
import time

class RaiRadioInfo:
    '''
    This class will add all the Radio stream I want
    To add new one I just have to follow the same syntax
    '''
        
    
    def __init__(self):

        self.streams_url = {

            "rairadio1": {
                "url": "http://icestreaming.rai.it/1.mp3",
                "logo": "/home/jack/Pictures/Logos/rai_radio_1.png"
                },

            "rairadio2": {
                "url": "http://icestreaming.rai.it/2.mp3",
                "logo": "/home/jack/Pictures/Logos/rai_radio_2.png"
                },

            "rairadio3": {
                "url": "http://icestreaming.rai.it/3.mp3",
                "logo": "/path/to/rai_radio_3_logo.png"
                },

            }


    def returning_stream(self, radio_name):
        self.radio_name = radio_name

        return self.streams_url[radio_name]['url'], self.streams_url[radio_name]['logo']
    

    def returning_list_id_channel(self) -> List:

        self.radio_id = []
        for radio_id in self.streams_url.keys():
            self.radio_id.append(radio_id)

        return self.radio_id
            

    def parsing_data(self):
        json_file = "onAir.json"
        self.url = "https://www.raiplaysound.it/palinsesto/onAir.json"
        
        # Check if the JSON file exists and is younger than 10 minutes (600 seconds)
        if os.path.exists(json_file):
            file_mod_time = os.path.getmtime(json_file)
            if time.time() - file_mod_time < 900:
                # If the file is less than 10 minutes old, load data from it
                with open(json_file, "r") as f:
                    self.data = json.load(f)
            else:
                # If the file is older than 10 minutes, fetch new data and overwrite the file
                self.response = requests.get(self.url)
                self.data = json.loads(self.response.text)
                with open(json_file, "w") as f:
                    json.dump(self.data, f)
        else:
            # If the file doesn't exist, fetch new data and create the file
            self.response = requests.get(self.url)
            self.data = json.loads(self.response.text)
            with open(json_file, "w") as f:
                json.dump(self.data, f)
        
        output = []
        description_channel = {}
        interval_time = {}
        
        # print(self.data['on_air'][0]['currentItem']['description'])


        for x in range(len(self.data['on_air'])):

            self.radio_name = self.data['on_air'][x]['currentItem']['channel']['name']
            if self.radio_name == "":
                self.radio_name = self.data['on_air'][x]['channel']
            try:
                self.program_name = (self.data['on_air'][x]['currentItem']['description']).lower()
            except:
                self.program_name = "None"
            try:
                self.time_interval = self.data['on_air'][x]['currentItem']['time_interval']
            except:
                self.time_interval = "Not available"

            output.append(f"{self.radio_name}")
            description_channel[self.radio_name.lower().strip().replace(' ', '').replace('è', 'e').replace('ü', 'u')] = self.program_name

            interval_time[self.radio_name.lower().strip().replace(' ', '').replace('è', 'e').replace('ü', 'u')] = self.time_interval

        return output, description_channel, interval_time

# print(RaiRadioInfo().parsing_data()[2])
