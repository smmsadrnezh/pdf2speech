# pdf2speech

You give this script a PDF file of the article. It will create a clean text in the form of a text file. The text in which the page headers have been deleted and the newlines are placed correctly. Then, it converts the text into an mp3 file and creates a summary text file using artificial intelligence.

## How to use

First, edit the `settings.py` file and change the `pdf_path` variable to the pdf file path you want to convert to speech. Here is the sample of the `settings.py` file:

```python
pdf_path = "document.pdf"
ignore_header_lines = 3
voice = "en-US-AriaNeural"
summary_min_length = 100
summary_max_length = 400
```

Run the script:

```bash
git clone https://github.com/smmsadrnezh/pdf2speech.git
cd pdf2speech
pip install -r requirements.txt
python main.py
```

It will produce a mp3 file in the same directory. It also generates a summary of the document and saves it in the same directory.
