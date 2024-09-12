import PyPDF2

# Open the PDF file in binary mode
with open('Costituzione_ITALIANO.pdf', 'rb') as pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''

    # Iterate over each page and extract text
    for page in reader.pages:
        text += page.extract_text()

# Save the extracted text to a .txt file
with open('Costituzione_ITALIANO.txt', 'w', encoding='utf-8') as txt_file:
    txt_file.write(text)