from abc import ABC, abstractmethod
import datetime
import json
import yaml
import glob
import re

one_year_from_now = datetime.datetime.now()
date_now = one_year_from_now.strftime("%d/%m/%Y")
data_dict = {
        "Date_es_:date": "",
        "Name": "",
        "Address_1": "",
        "Address_2": "",
        "Address_3": "",
        "Address_4": "",
        "Address_5": "",
        "Address_6": "",
        "Postal_code": "",
        "Phone_Number": ""
    }

class inputFile(ABC):

    @abstractmethod
    def __init__(self, input):
        self.input_file = input

    @abstractmethod
    def readFile(self):
        pass

class inputJson(inputFile):
    def __init__(self, input):
        super().__init__(input)


    def readFile(self):
        self.data_dict = {}
        with open( self.input_file, encoding="utf-8") as file:
            data = json.load(file)
            for i in data["txt_fill"]:
                self.data_dict = i
                if self.data_dict["Date_es_:date"] == "":
                    self.data_dict["Date_es_:date"] = str(date_now)
            file.close()
        return self.data_dict

class inputText(inputFile):

    def __init__(self, input):
        super().__init__(input)
    
    def readFile(self):
        txt_file = self.input_file
        with open(txt_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            text = ""
            for line in lines:
                #print(line)
                text += line
                text_list = text.split("\n")
                #print(text_list)
            file.close()
        i = 0
        for key in data_dict.keys():
            if key == "Date_es_:date":
                data_dict[key] = str(date_now)
            else:
                data_dict[key] = text_list[i]
                i += 1
            if i == len(text_list):
                break
        #print(data_dict)
        return data_dict

class inputYml(inputFile):

    def __init__(self, input):
        super().__init__(input)
    
    def readFile(self):
        self.data_dict = {}
        with open( self.input_file, encoding="utf-8") as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            for i in data["txt_fill"]:
                self.data_dict = i
                if self.data_dict["Date_es_:date"] == "":
                    self.data_dict["Date_es_:date"] = str(date_now)
            file.close()
        return self.data_dict
