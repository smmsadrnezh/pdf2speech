from transformers import BartForConditionalGeneration, BartTokenizer
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import edge_tts
import asyncio

pdf_path = "document.pdf"
ignore_header_lines = 3
voice = "en-US-AriaNeural"
summary_min_length = 100
summary_max_length = 400


def summarize_article(text_path):
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    with open(text_path, 'r') as f:
        inputs = tokenizer.encode("summarize: " + f.read(), return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=summary_max_length, min_length=summary_min_length, length_penalty=2.0, num_beams=4,
                                 early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    with open(text_path.replace('.txt', '_summary.txt'), 'w') as f:
        f.write(summary)


def text_to_voice(text_path, voice_path):
    with open(text_path, 'r') as f:
        communicate = edge_tts.Communicate(f.read(), voice)
        asyncio.run(communicate.save(voice_path))


def fix_text(text_path, fix_path):
    def num_words_line(line):
        return len(line.split())

    def iter_lines(input_file):
        with open(input_file) as f:
            previous = next(f)
            for line in f:
                if '' in previous:
                    for _ in range(ignore_header_lines):
                        previous = next(f)
                yield (previous, line)
                previous = line
            yield line, None

    with open(fix_path, "w") as fout:
        for line, next_line in iter_lines(text_path):
            if (next_line is not None and
                    num_words_line(line) > 1 and
                    num_words_line(next_line) > 0):
                line = line.replace("-\n", "").replace("\n", " ")
            fout.write(line)


def main(pdf_path):
    text_path = pdf_path.replace('.pdf', '.txt')
    with open(pdf_path, 'rb') as pdf_file, open(text_path, 'w') as text_file:
        extract_text_to_fp(pdf_file, text_file, laparams=LAParams(), strip_control=True)

    fix_path = text_path.replace('.txt', '_fixed.txt')
    fix_text(text_path, fix_path)

    voice_path = pdf_path.replace('.pdf', '.mp3')
    text_to_voice(fix_path, voice_path)

    summarize_article(fix_path)


if __name__ == '__main__':
    main(pdf_path)
