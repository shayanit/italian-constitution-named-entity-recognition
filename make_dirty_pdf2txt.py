import PyPDF2, re

# Open the PDF file in binary mode
with open('data/Costituzione_ITALIANO.pdf', 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    content = ''
    for page in reader.pages:
        text = page.extract_text()
        # Remove the running header of every page
        lines = text.split('\n')
        trimmed_lines = [line.rstrip() for line in lines]
        text = '\n'.join(trimmed_lines[1:])
        # Remove hyphenations that split words across lines
        # Example: "perequa -\ntivo" becomes "perequativo"
        text = re.sub(r' -\n', '', text)
        content += text + "\n"
    content = content.replace("\n", " ")

# Save the extracted text to a .txt file
with open('data/Costituzione_ITALIANO_dirty.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(content)

