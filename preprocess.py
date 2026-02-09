import os
import re
from bs4 import BeautifulSoup
import tqdm

#%% s


def process_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    if not soup.find('span', class_=re.compile('^ChapterContent_label')):
        print("Empty or invalid content, skipping file.")
        return None

    book_label = soup.find('span', class_=re.compile('^ChapterContent_label')).text.strip()
    title = soup.find('h1').text.strip()
    headings = soup.find_all('span', class_=re.compile('^ChapterContent_heading'))
    # verses
    verses = soup.find_all('span', class_=re.compile('^ChapterContent_verse'))
    ids  = list({s.get('data-usfm') for s in verses if s.get('data-usfm')})

    verse_data_list = []
    for id in ids:

        #id = verse.get('data-usfm', '').strip()
        print('ID:', id)
        
        verse_label = 'N/A'  # Default value if label is not found
        inner_verses = soup.find_all('span', {'class': re.compile('^ChapterContent_verse'), 'data-usfm': id})
        contents = []
        for inner_verse in inner_verses:
            label_span = inner_verse.find('span', class_=re.compile('^ChapterContent_label'))
            if label_span:
                verse_label = label_span.text.strip()
            contents.extend(inner_verse.find_all('span', class_=re.compile('^ChapterContent_content')))
        text = [a.text.strip() for a in contents]
        verse_data_list.append({
            'id': id,
            'label': verse_label,
            'text': text
        })

    verse_data = {
        'book_label': book_label,
        'title': title,
        'headings': [h.text.strip() for h in headings],
        'verses': verse_data_list
    }

    return verse_data


def preprocess_data(data_dir):
    """Preprocess HTML files in the given directory."""
    from bs4 import BeautifulSoup
    import os

    data = []
    for filename in tqdm.tqdm(os.listdir(data_dir), disable=True):
        if filename.endswith('.html'):
            try:
                file_path = os.path.join(data_dir, filename)
                print(f"Processing file: {file_path}")
                verse_data = process_html_file(file_path)
                if verse_data:
                    data.append(verse_data)
                else:
                    print(f"No valid content found in file: {file_path}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                break
    # Save the data to a json file
    with open(os.path.join(data_dir, "processed_data.json"), 'w', encoding='utf-8') as file:
        import json
        json.dump(data, file, ensure_ascii=False, indent=4)
                


if __name__ == "__main__":
    data_directory = os.path.join("data", "BHTI_es")
    #data_directory = os.path.join("data", "toba")
    preprocess_data(data_directory)


