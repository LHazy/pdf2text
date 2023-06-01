import os
import argparse

from langchain import OpenAI, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

from pdf2image import convert_from_path
from pytesseract import image_to_string, get_languages

from dotenv import load_dotenv
load_dotenv()


def pdf2images(pdf_file):
    images = convert_from_path(pdf_file)
    return images


def images2text(images, lang='eng'):
    text = ''
    for image in images:
        text += image_to_string(image, lang)
    return text


def pdf2text(pdf_file, lang):
    images = pdf2images(pdf_file)
    text = images2text(images, lang)
    return text


def summarize(long_text):
    llm = OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY')) # type: ignore
    splitter = CharacterTextSplitter()
    texts = splitter.split_text(long_text)
    
    docs = [Document(page_content=t) for t in texts]

    chain = load_summarize_chain(llm=llm, chain_type="map_reduce", return_intermediate_steps=True)
    return chain(docs)['output_text']


def translate(text, from_lang, to_lang):
    # chat = ChatOpenAI(temperature=0, model_name="gpt-4", openai_api_key=os.getenv('OPENAI_API_KEY'))
    chat = ChatOpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY')) # type: ignore
    template = "You are a helpful assistant that translates {from_lang} to {to_lang}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    chain = LLMChain(llm=chat, prompt=chat_prompt)

    splitter = CharacterTextSplitter()
    texts = splitter.split_text(text)
    results = []
    for t in texts:    
        result = chain.run(from_lang=from_lang, to_lang=to_lang, text=t)
        results.append(result)

    return ''.join(results)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='input file', required=True, dest='inputfile')
    parser.add_argument('-o', '--output', help='output file', required=True, dest='outputfile')
    parser.add_argument('-s', '--summarize', help='summarize text', action='store_true')
    parser.add_argument('-l', '--lang', help='language', default='eng')
    parser.add_argument('-t', '--translate', help='translate text from <lang> to <lang>', nargs=2)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()

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

    if args.translate:
        from_lang = args.translate[0]
        to_lang = args.translate[1]

        print(f'Start translate: {from_lang} -> {to_lang}')
        text = translate(text, from_lang, to_lang)
        print(f'Finished translate.')

    if args.summarize:
        print(f'Start summarize...')
        text = summarize(text)
        print(f'Finished summarize.')
    
    with open(args.outputfile, 'w') as f:
        f.write(text)
    print(f'Output: {args.outputfile}')
