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

# Usage
## help
```
usage: pdf2text.py [-h] -i INPUTFILE -o OUTPUTFILE [-s] [-l LANG]

options:
  -h, --help            show this help message and exit
  -i INPUTFILE, --input INPUTFILE
                        input file
  -o OUTPUTFILE, --output OUTPUTFILE
                        output file
  -s, --summarize       summarize text
  -l LANG, --lang LANG  language
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