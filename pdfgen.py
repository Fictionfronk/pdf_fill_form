import argparse
import pdfrw
import datetime
import json


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to the input .json format file")
ap.add_argument("-o", "--output", required=True, help="output file name .pdf format file")
ap.add_argument("-t", "--template", required=True, help="template file (.pdf format file")
ap.add_argument("-f", "--font", required=True, help="font file name .ttf format file")
args = vars(ap.parse_args())

data_dict = {}
one_year_from_now = datetime.datetime.now()
date_now = one_year_from_now.strftime("%d/%m/%Y")

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

class PDFgen:

    def __init__(self, option):
        self.option = option
        if ".่json" in self.option["input"]:
            self.input = self.option["input"]
        if ".pdf" in self.option["output"]:
            self.output = self.option["output"]
        if ".pdf" in self.option["template"]:
            self.template = self.option["template"]
        if ".ttf" in self.option["font"]:
            self.font = self.option["font"]

    def getInputCommand(self):
        return self.input, self.output, self.template, self.font

    def readJson(self):
        self.data_dict = {}
        with open(self.input, encoding='utf-8') as file:
            data = json.load(file)
            for i in data['txt_fill']:
                self.data_dict = i
                if self.data_dict["Date_es_:date"] == "":
                    self.data_dict["Date_es_:date"] = str(date_now)
            file.close()
        return self.data_dict

    def fill_pdf(self, template):
        for page in template.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        #print(key)
                        if key in data_dict.keys():
                            #print(data_dict[key])
                            annotation.update(pdfrw.PdfDict(V='{}'.format(data_dict[key])))
                            annotation.update(pdfrw.PdfDict(AP=''))
        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfFileWriter().write(self.output, template)


if __name__ == '__main__':
    command = PDFgen(args)
    json_input, pdf_output, pdf_template, font_input = command.getInputCommand()

    pdf_template = pdfrw.PdfReader(pdf_template)

    data_dict = command.readJson()
    command.fill_pdf(pdf_template)

