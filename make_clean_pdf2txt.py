import PyPDF2, re

# Open the PDF file in binary mode
with open('data/Costituzione_ITALIANO.pdf', 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    content = ''

    # Iterate over each page and extract text and clean it
    for page in reader.pages:
        text = page.extract_text()
        # Remove the running header of every page
        lines = text.split('\n')
        trimmed_lines = [line.rstrip() for line in lines]
        text = '\n'.join(trimmed_lines[1:])
        # Remove the footer in every page
        parts = text.split("(*) ")
        text = parts[0]
        parts = text.split("1 Cost. ")
        text = parts[0]
        # Remove hyphenations that split words across lines
        # Example: "perequa -\ntivo" becomes "perequativo"
        text = re.sub(r' -\n', '', text)
        # Replace newlines that break sentences with a space
        # (if a line ends without punctuation and the next line starts with a lowercase letter)
        text = re.sub(r'([^\.\!\?])\n([a-zàèéìòù])', r'\1 \2', text)
        # Remove superscript numbers that are attached to words
        text = re.sub(r'(?<=[^\s\d])\d+(?=\.)', '', text)
        text = re.sub(r'(?<=\S)\d+(?=\s)', '', text)
        content += text + "\n"

# Save the extracted text to a .txt file
with open('data/Costituzione_ITALIANO_clean.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(content)