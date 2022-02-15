from argparse import ArgumentParser
from os.path import splitext
from pdf2image import convert_from_path
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from tempfile import mkdtemp
from uuid import uuid4


def concatenate_images_to_pdf(
    images,
    background_color,
    align,
    output_pdf_filename
):
    images_to_concatenate = list()
    for image in images:
        images_to_concatenate.append(Image.open(image))

    widths = list()
    heights = list()
    for image in images_to_concatenate:
        widths.append(image.width)
        heights.append(image.height)

    output_pdf_width = max(widths)
    output_pdf = Image.new(
        "RGB",
        (output_pdf_width, sum(heights)),
        background_color
    )
    image_index = 0
    for image in images_to_concatenate:
        if align == "left":
            x_pos = 0
        elif align == "center":
            x_pos = round((output_pdf_width - widths[image_index]) / 2)
        elif align == "right":
            x_pos = output_pdf_width - widths[image_index]
        y_pos = 0 if image_index == 0 else sum(heights[0:image_index])
        output_pdf.paste(image, (x_pos, y_pos))
        image_index += 1
    output_pdf.save(output_pdf_filename, "PDF")


def convert_pdfs_to_images(pdfs):
    images = list()
    for pdf in pdfs:
        for image in convert_from_path(pdf):
            image_path = f"{tmp}/{uuid4()}.png"
            image.save(image_path, "PNG")
            images.append(image_path)
    return images


def extract_pages(pdfs, num_of_pages):
    new_pdfs = list()
    for pdf in pdfs:
        new_pdf_path = f"{tmp}/{uuid4()}.pdf"
        with open(pdf, "rb") as r:
            orig_pdf = PdfFileReader(r)
            new_pdf = PdfFileWriter()
            for page in range(num_of_pages):
                new_pdf.addPage(orig_pdf.getPage(page))
            with open(new_pdf_path, "wb") as w:
                new_pdf.write(w)
        new_pdfs.append(new_pdf_path)
    return new_pdfs


if __name__ == "__main__":
    parser = ArgumentParser(prog="pdf4gmk")
    parser.add_argument(
        "pdfs",
        type=str,
        help="comma-separated list of PDFs"
    )
    parser.add_argument(
        "pages",
        type=int,
        help="number of pages to extract from the PDFs",
    )
    parser.add_argument(
        "--align",
        default="left",
        type=str,
        required=False,
        help="page alignment (left, center or right)"
    )
    parser.add_argument(
        "--color",
        default="255,255,255",
        type=str,
        required=False,
        help="background color in an R,G,B format"
    )
    args = parser.parse_args()

    pdfs = args.pdfs.split(",")
    bg_color = tuple((int(_) for _ in args.color.split(",")))
    align = args.align.lower()
    output_pdf_filename = \
        "pdf4gmk_" + \
        "".join([splitext(_)[0] for _ in pdfs]) + \
        ".pdf"

    tmp = mkdtemp()
    tmp_pdfs = extract_pages(pdfs, args.pages)
    tmp_images = convert_pdfs_to_images(tmp_pdfs)
    concatenate_images_to_pdf(
        tmp_images,
        bg_color,
        align,
        output_pdf_filename
    )
    print(f"Output saved to: {output_pdf_filename}")
