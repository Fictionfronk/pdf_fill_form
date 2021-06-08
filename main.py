import pdfgen
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--input", required=True, help="path to the input .json or .txt or .yml format file"
    )
    ap.add_argument(
        "-o", "--output", required=True, help="output file .pdf format file"
    )
    ap.add_argument(
        "-t", "--template", required=True, help="template file .pdf format file"
    )
    args = vars(ap.parse_args())

    command = pdfgen.PDFgen(args)
    _, _, pdf_template = command.getInputCommand()

    pdf_template = command.readPDF(pdf_template)

    if ".json" in args["input"]:
        data_dict = command.readJson()
    elif ".txt" in args["input"]:
        data_dict = command.readText()
    elif ".yml" in args["input"]:
        data_dict = command.readYml()

    command.fill_pdf(pdf_template, data_dict)
    print("done!")