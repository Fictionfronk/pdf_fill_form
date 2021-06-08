import pdfgen
import argparse

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "-i", "--input", required=True, help="path to the input .json format file"
    )
    ap.add_argument(
        "-o", "--output", required=True, help="output file name .pdf format file"
    )
    ap.add_argument(
        "-t", "--template", required=True, help="template file (.pdf format file"
    )
    args = vars(ap.parse_args())

    command = pdfgen.PDFgen(args)
    input, pdf_output, pdf_template = command.getInputCommand()

    pdf_template = command.readPDF(pdf_template)

    data_dict = command.readJson()
    command.fill_pdf(pdf_template, data_dict)
    print("done!")