import os
import argparse


from pdf2image import convert_from_path
from pytesseract import image_to_string, get_languages


# convert pdf to images
def pdf2images(pdf_file):
    # convert pdf to images
    images = convert_from_path(pdf_file)
    return images


# read text from images
def images2text(images, lang='eng'):
    # read text from images
    text = ''
    for image in images:
        text += image_to_string(image, lang)
    return text


# read text from pdf
def pdf2text(pdf_file, lang):
    # read text from pdf
    images = pdf2images(pdf_file)
    text = images2text(images, lang)
    return text


# parse arguments
# pdf2text.py -i <inputfile> -o <outputfile>
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file', required=True, dest='inputfile')
    parser.add_argument('-o', '--output', help='output file', required=True, dest='outputfile')
    parser.add_argument('-l', '--lang', help='language', default='eng')
    args = parser.parse_args()
    return args


# main
if __name__ == '__main__':
    args = parse_args()

    # check file existence
    if not os.path.exists(args.inputfile):
        print('Input file not found.')
        exit(1)
    
    # get all supported languages from tesseract
    langs = get_languages(config='')
    if args.lang not in langs:
        print('Language not supported.')
        print(f'Supported languages are: {langs}')
        exit(1)

    print(f'Processing {args.inputfile}...')
    text = pdf2text(args.inputfile, args.lang)
    print(f'Finished processing.')

    with open(args.outputfile, 'w') as f:
        f.write(text)
    print(f'Output: {args.outputfile}')
