import os
import re
from bs4 import BeautifulSoup
import tqdm

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
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')

                if not soup.find('span', class_=re.compile('^ChapterContent_label')):
                    print("Empty or invalid content, skipping file.")
                    continue

                book_label = soup.find('span', class_=re.compile('^ChapterContent_label')).text.strip()
                title = soup.find('h1').text.strip()
                headings = soup.find_all('span', class_=re.compile('^ChapterContent_heading'))
                # verses
                verses = soup.find_all('span', class_=re.compile('^ChapterContent_verse'))

                verse_data_list = []
                for verse in verses:

                    id = verse.get('data-usfm', '').strip()
                    print('ID:', id)
                    verse_label = verse.find('span', class_=re.compile('^ChapterContent_label')).text.strip()
                    print(verse_label)
                    text = ''.join([a.text.strip() for a in verse.find_all('span', class_=re.compile('^ChapterContent_content'))])
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

                data.append(verse_data)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                break
    # Save the data to a json file
    with open(os.path.join(data_dir, "processed_data.json"), 'w', encoding='utf-8') as file:
        import json
        json.dump(data, file, ensure_ascii=False, indent=4)
                


if __name__ == "__main__":
    data_directory = os.path.join("data", "BHTI_es")
    preprocess_data(data_directory)