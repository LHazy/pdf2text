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
* simple
```bash
python pdf2text.py -i  /home/user/Downloads/hello.pdf -o hello.txt 
```
* specify language
```bash
python pdf2text.py -i  /home/user/Downloads/hello.pdf -o hello.txt -l eng
```
