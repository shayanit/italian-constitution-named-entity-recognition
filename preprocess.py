import re

def clean_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Remove hyphenations that split words across lines
    # Example: "perequa -\ntivo" becomes "perequativo"
    text = re.sub(r'-\n', '', text)

    # Replace newlines that break sentences with a space
    # (if a line ends without punctuation and the next line starts with a lowercase letter)
    text = re.sub(r'\n(?!\n)(?=[a-zà-ú])', ' ', text)

    # Remove all remaining single newlines, except double newlines (which denote paragraph breaks)
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)

    # Write the cleaned text to a new file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(text)

    print(f"Text has been successfully cleaned and saved to {output_file}")

# Call the function
clean_text('Costituzione_ITALIANO.txt', 'Costituzione_ITALIANO_clean.txt')
