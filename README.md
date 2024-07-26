# pdf2speech

First, edit the `settings.py` file and change the `pdf_path` variable to the pdf file path you want to convert to speech. Here is the sample of the `settings.py` file:

```python
pdf_path = "document.pdf"
ignore_header_lines = 3
voice = "en-US-AriaNeural"
summary_min_length = 100
summary_max_length = 400
```

How to use:

```bash
git clone https://github.com/smmsadrnezh/pdf2speech.git
cd pdf2speech
pip install -r requirements.txt
python main.py
```

It will produce a mp3 file in the same directory. It also generates a summary of the document and saves it in the same directory.
