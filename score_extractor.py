#%%
from PIL import Image
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

import re
import pytesseract

from tqdm import tqdm


#%%
def num_to_bgw(num):
    high = 254
    low = 75
    
    if num >= high:
        return 'w'
    elif num < high and num >= low:
        return 'g'
    elif num < low:
        return 'b'
    else:
        return 'w'


def letterize(img, thresh=200):
    dat = np.array(img.convert(mode='L'))
    h, w = dat.shape
    
    dat = dat.mean(axis=1)
    plt.plot(dat*(dat>thresh))

    vf = np.vectorize(num_to_bgw)
    return ''.join(vf(dat))
    

def get_intervals(letterized, px=45, pad=5):

    pattern = 'w{' + str(px) + ',}'
    brk = re.compile(pattern)

    intervals = []
    start = 0

    for match in re.finditer(brk, letterized):
        interval = [0,0]
        if start != len(letterized) and start:
            interval[0] = start - pad
        fin, start = match.span()
        if fin:
            interval[1] = fin + pad
        interval = tuple(interval)
        if interval != (0,0):
            intervals.append(interval)
    
    return intervals


def return_score_intervals(intervals, letterized):
    new_intervals = []
    for interval in intervals:
        upper, lower = interval
        segment = letterized[upper: lower]
        pattern = 'b\w+b\w+b\w+b'
        if re.search(pattern, segment):
            new_intervals.append(interval)
    return new_intervals


def return_score_images(img, intervals):
    dat = np.array(img.convert(mode='L'))
    h, w = dat.shape

    imgs = []
    for interval in intervals:
        upper, lower = interval
        box = (0, upper, w, lower)
        imgs.append(img.crop(box))
    return imgs


def cleanup(lines):
    pattern = re.compile(r'^\s*$')
    return [line for line in lines if not re.match(pattern, line)]


def get_title(score):
    ocr_text = pytesseract.image_to_string(score)
    lines = cleanup(ocr_text.split('\n'))
    top_lines = lines[0:2]

    pattern = re.compile(r'[^\w\d\s-]')

    top_lines = [line for line in top_lines if not re.search(pattern, line)]

    return ' - '.join(top_lines)


def save_score(score, loc):
    title = get_title(score)

    n = 1
    path = Path(loc, title + ' (Version ' + str(n) + ').gif')    
    while path.exists():
        n += 1
        path = Path(loc, title + ' (Version ' + str(n) + ').gif')    

    score.save(path)


def extract_and_save_score(fn, score_fldr):
    img = Image.open(fn)
    letterized = letterize(img, thresh=200)
    intervals = get_intervals(letterized, px=45, pad=15)
    intervals = return_score_intervals(intervals, letterized)
    scores = return_score_images(img, intervals)
    for score in scores:
        save_score(score, score_fldr)

#%%

if __name__ == '__main__':
    or_img_fldr = Path('Images', 'originals')
    score_fldr = Path('Images', 'scores')
    imgs = [fn for fn in or_img_fldr.glob('**/*.gif')]
    for fn in tqdm(imgs):
        extract_and_save_score(fn, score_fldr)
# %%
