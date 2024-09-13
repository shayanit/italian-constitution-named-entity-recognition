from tqdm import tqdm
from openai import OpenAI

def correct_split_words(text):
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": f"Correct the following text and fix any split words. Don't change line breaks. Output only the corrected text: {text}"
            }
        ]
    )

    return completion.choices[0].message.content

text = ''
with open('data/Costituzione_ITALIANO_clean.txt', 'r', encoding='utf-8') as f:
    text = f.read()
articles = text.split('Art.')

# Adding back 'Art.' to each article and stripping leading/trailing spaces
articles = ['Art.' + article for article in articles if article]

content = ""
for article in tqdm(articles):
    content += correct_split_words(article) + "\n"

with open('data/Costituzione_ITALIANO_cleaner.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(content)