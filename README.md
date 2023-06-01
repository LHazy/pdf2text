# Install
## Ubuntu
1. install tesseract
```bash
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```
2. install pip
```bash
pip install -r requirements.txt
```
3. setup openai
```console
cp .env.sample .env
# and paste api key to .env
```

# Usage
## help
```
usage: pdf2text.py [-h] -i INPUTFILE -o OUTPUTFILE [-s] [-l LANG] [-t TRANSLATE TRANSLATE]

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file
  -o OUTPUTFILE, --output OUTPUTFILE
                        output file
  -s, --summarize       summarize text
  -l LANG, --lang LANG  language
  -t TRANSLATE TRANSLATE, --translate TRANSLATE TRANSLATE
                        translate text from <lang> to <lang>
```
## samples
* simple
```bash
python pdf2text.py -i /home/user/Downloads/hello.pdf -o hello.txt
```
* specify language
```bash
python pdf2text.py -i /home/user/Downloads/hello.pdf -o hello.txt -l eng
```
* summarize
```bash
python pdf2text.py -s -i /home/user/Downloads/hello.pdf -o hello.txt -l eng
```
* translate
```bash
python pdf2text.py -i /home/user/Downloads/hello.pdf -o hello.txt -l eng -t english japanese
```