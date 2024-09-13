# Problem 3

The goal is to extract a list of entities from the Italian Constitution. I organized the project into the following steps:

## PDF to Text Conversion
Using `make_clean_pdf2txt.py`, I extracted the content of each page, removed headers and footnotes, applied basic regular expressions for text cleaning, and saved the results to `Costituzione_ITALIANO_clean.txt`. The text is mostly clean, though some words are incorrectly split with a space. For instance, "cattolico" might appear as "ca tolico."

## Correcting Split Words with LLM
With `Llama_3_1_8B_correct_split_words.ipynb`, I tested `Meta Llama 3.1 8B` for correcting split words, but while it performed well, a single inference on a Colab T4 GPU took about 5 minutes. To speed up inference and considering the low cost of serverless inference APIs (a few cents for around 80,000 characters or 20,000 tokens based on OpenAI's approximately 4 character per token), I decided to use OpenAI's `GPT-4 mini`.

Using `make_cleaner_correct_split_words.py`, I processed each "Art." section with OpenAI's `GPT-4 mini` to correct split words, producing a near-perfect version of the text. The cleaned output was saved to `Costituzione_ITALIANO_cleaner.txt`. The cost was a few cents as expected.

## Entity Extraction with Regular Expressions
I used `re_find_entities.py` to identify entities using regular expressions in the text and saved them to `re_entities.json`.

## Entity Extraction with Named Entity Recognition (NER)
Using `ner_find_entities.py`, I applied spaCy's NER model to extract entities, saving the results in `ner_entities.json`. This method is more reliable than regular expressions, as it leverages NLP techniques for more accurate entity identification.

## Bonus: Extracting Regulatory References
### Dirty PDF to Text Conversion
Using `make_dirty_pdf2txt.py`, I converted the entire PDF—including footnotes—into text. I cleaned the resulting file by fixing words split by hyphens across lines and applying other minor corrections.

### Extracting Regulatory References with Regular Expressions
Finally, with `re_find_regulatory_references.py`, I identified regulatory references in the Italian Constitution using regular expressions and saved them to `regulatory_references.json`.