import re

def clean_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
        
    lines = text.split('\n')

    # Remove trailing spaces from each line
    cleaned_lines = [line.rstrip() for line in lines]
    
    text = '\n'.join(cleaned_lines)
        
    # Remove footnotes
    text = re.sub(r"\(\*\) .+?(?=Costituzione della Repubblica Italiana_Layout)", "(*)", text, flags=re.DOTALL)
    text = re.sub(r"1 Cost\..*?(?=Costituzione della Repubblica Italiana_Layout)", '', text, flags=re.DOTALL)
    text = re.sub(r"\(\*\)", '', text, flags=re.DOTALL)

    # Remove hyphenations that split words across lines
    # Example: "perequa -\ntivo" becomes "perequativo"
    text = re.sub(r'-\n', '', text)

    # Replace newlines that break sentences with a space
    # (if a line ends without punctuation and the next line starts with a lowercase letter)
    text = re.sub(r'([^\.\!\?])\n([a-zàèéìòù])', r'\1 \2', text)

    # # Remove all remaining single newlines, except double newlines (which denote paragraph breaks)
    # text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    
    #remove page number after running header
    text = re.sub(r"(COSTITUZIONE  DELLA  REPUBBLICA  ITALIANA)\s*\d*", r"\1", text)
    
    #remove page info
    #re.sub(pattern, replacement, text, flags=re.DOTALL)
    text = re.sub(r'(Costituzione della Repubblica Italiana_Layout 1.*?COSTITUZIONE\s+DELLA\s+REPUBBLICA\s+ITALIANA)', "", text, flags=re.DOTALL)
    
    #remove double spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    #remove superscript numbers that are attached to words
    re.sub(r'(\d+)(?=\w)|(?<=\w)(\d+)([ .]?)', '', text)

    # Write the cleaned text to a new file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        f_out.write(text)

    print(f"Text has been successfully cleaned and saved to {output_file}")

# Call the function
clean_text('Costituzione_ITALIANO.txt', 'Costituzione_ITALIANO_clean.txt')
