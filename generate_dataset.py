import os, random
from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm

CORPUS = 'corpus.txt'
FONT_DIR = "fonts"
OUTPUT = "data"
NUM_SAMPLES = 50000
LABELS = os.path.join(OUTPUT, 'labels.txt')

SIZE = (768,384)
FONT_SIZE = 27
LINE_SPACING  = 10

LEFT_PADDING = 20
RIGHT_PADDING = 20
TOP_PADDING = 20
BOTTOM_PADDING = 20

MAX_TEXT_WIDTH = SIZE[0] - LEFT_PADDING - RIGHT_PADDING
MAX_TEXT_HEIGHT = SIZE[1] - TOP_PADDING - BOTTOM_PADDING

os.makedirs(os.path.join(OUTPUT, 'images'), exist_ok=True)

fonts = [os.path.join(FONT_DIR,f) for f in os.listdir(FONT_DIR) if f.endswith(('.ttf','.otf'))]

with open(CORPUS, 'r', encoding = 'utf-8') as cor:
    corpus_lines = [line.strip() for line in cor if line.strip()]

def fit_line_to_width(text, font, max_width):
    current_width = 0
    fitted_chars = []
    for char in text:
        char_width = font.getlength(char)
        if current_width + char_width > max_width:
            break
        fitted_chars.append(char)
        current_width += char_width
    return "".join(fitted_chars).strip()

with open(LABELS, 'w', encoding = 'utf-8') as label_file:
    for i in tqdm(range(NUM_SAMPLES)):
        path_font_to_use = random.choice(fonts)
        font = ImageFont.truetype(path_font_to_use, FONT_SIZE)

        img = Image.new('RGB',SIZE, (255,255,255))
        draw = ImageDraw.Draw(img)

        num_lines = random.randint(2,8)
        selected_lines_to_use = random.sample(corpus_lines,num_lines)
        y_off = TOP_PADDING
        drawn_lines = []

        for l in selected_lines_to_use:
            if y_off + FONT_SIZE > SIZE[1] - BOTTOM_PADDING:
                break
            fitted_text = fit_line_to_width(l, font,MAX_TEXT_WIDTH)
            if fitted_text:
                draw.text((LEFT_PADDING,y_off), fitted_text, fill=(0,0,0), font = font)
                drawn_lines.append(fitted_text)
                y_off += FONT_SIZE + LINE_SPACING
        img.save(os.path.join(OUTPUT, 'images', f'img{i}.png'))
        truth = "\\n".join(selected_lines_to_use)
        label_file.write(f'images/img{i}.png\t{truth}\n')

print('DONE')