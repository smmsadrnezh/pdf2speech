from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import edge_tts
import asyncio

pdf_path = "document.pdf"

def text_to_voice(text_path, voice_path):
    VOICE = "en-GB-SoniaNeural"

    with open(text_path, 'r') as f:
        communicate = edge_tts.Communicate(f.read(), VOICE)
        asyncio.run(communicate.save(voice_path))


def fix_text(text_path, fix_path):
    ignore_lines = 3

    def num_words_line(line):
        return len(line.split())

    def iter_lines(input_file):
        with open(input_file) as f:
            previous = next(f)
            for line in f:
                if '' in previous:
                    for _ in range(ignore_lines):
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

if __name__ == '__main__':
    main(pdf_path)
