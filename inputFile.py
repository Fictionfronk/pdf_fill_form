from abc import ABC, abstractmethod
import datetime
import json

one_year_from_now = datetime.datetime.now()
date_now = one_year_from_now.strftime("%d/%m/%Y")

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
        return super().readFile()

class inputYml(inputFile):

    def __init__(self, input):
        super().__init__(input)
    
    def readFile(self):
        return super().readFile()
