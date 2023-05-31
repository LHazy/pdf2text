import os
import argparse

from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

from pdf2image import convert_from_path
from pytesseract import image_to_string, get_languages

from dotenv import load_dotenv
load_dotenv()


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
    parser.add_argument('-s', '--summarize', help='summarize text', action='store_true')
    parser.add_argument('-l', '--lang', help='language', default='eng')
    args = parser.parse_args()
    return args


# summarize text
def summarize(long_text):
    llm = OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY')) # type: ignore
    splitter = CharacterTextSplitter()
    texts = splitter.split_text(long_text)
    
    docs = [Document(page_content=t) for t in texts]

    chain = load_summarize_chain(llm=llm, chain_type="map_reduce", return_intermediate_steps=True)
    return chain(docs)['output_text']


# main
if __name__ == '__main__':
    args = parse_args()

    # check file existence
    if not os.path.exists(args.inputfile):
        print('Input file not found.')
        exit(1)
    
    langs = get_languages(config='')
    if args.lang not in langs:
        print('Language not supported.')
        print(f'Supported languages are: {langs}')
        exit(1)

    print(f'Start convert: {args.inputfile}...')
    text = pdf2text(args.inputfile, args.lang)
    print(f'Finished convert.')

    if args.summarize:
        print(f'Start summarize...')
        text = summarize(text)
        print(f'Finished summarize.')

    with open(args.outputfile, 'w') as f:
        f.write(text)
    print(f'Output: {args.outputfile}')
