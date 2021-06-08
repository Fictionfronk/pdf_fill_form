import pdfrw
import datetime
import inputFile

data_dict = {}
one_year_from_now = datetime.datetime.now()
date_now = one_year_from_now.strftime("%d/%m/%Y")

ANNOT_KEY = "/Annots"
ANNOT_FIELD_KEY = "/T"
ANNOT_VAL_KEY = "/V"
ANNOT_RECT_KEY = "/Rect"
SUBTYPE_KEY = "/Subtype"
WIDGET_SUBTYPE_KEY = "/Widget"


class PDFgen:
    def __init__(self, option):
        #print(option["input"])
        if ".json" in option["input"]:
            self.input = option["input"]
        if ".pdf" in option["output"]:
            self.output = option["output"]
        if ".pdf" in option["template"]:
            self.template = option["template"]
        #print(self.input, self.output, self.template)

    def getInputCommand(self):
        return self.input, self.output, self.template

    def readPDF(self, template):
        return pdfrw.PdfReader(template)

    def readJson(self):
        self.data_dict = {}
        self.data_dict = inputFile.inputJson(self.input).readFile()
        return self.data_dict

    def fill_pdf(self, template, data):
        for page in template.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        # print(key)
                        if key in data.keys():
                            # print(data_dict[key])
                            annotation.update(
                                pdfrw.PdfDict(V="{}".format(data[key]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=""))
        template.Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject("true"))
        )
        pdfrw.PdfFileWriter().write(self.output, template)
