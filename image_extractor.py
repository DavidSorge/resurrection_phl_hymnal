#%%
from pathlib import Path
from pdf2image import convert_from_path
from tqdm import tqdm


#%%
def convert_to_images(filepath):
    pages = convert_from_path(filepath)
    for i in range(len(pages)):
        name = f'{"_".join(str(filepath.stem).split())}_page_{i+1}.gif'
        pages[i].save(Path('Images', 'originals', name), 'gif')

# %%
if __name__ == '__main__':
    here = Path('.')
    pdfs = [x for x in here.glob('**/*.pdf')]

    for filepath in tqdm(pdfs):
        convert_to_images(filepath)
        print('Unpacked', filepath.stem)