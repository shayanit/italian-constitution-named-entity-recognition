# Problem 3

The objective is to extract a list of entities from the Italian Constitution PDF. The project was done by following these steps:

## Initial experiments
Initial tests revealed that a simple text extraction from the PDF was insufficient. The resulting text was disorganized, with footnotes and headers interrupting the main content, making it difficult to comprehend. While I could find some of the entities in the text, it was obvious that some of them are lost in the chaos. Recognizing the truth behind the phrase "garbage in, garbage out," I decided to clean the text thoroughly before attempting to extract any meaningful information. This approach ensured a more accurate and reliable extraction process.

## PDF to Text Conversion
Using [make_clean_pdf2txt.py](make_clean_pdf2txt.py), I extracted the content of each page, removed headers and footnotes, applied basic regular expressions for text cleaning, and saved the results to [Costituzione_ITALIANO_clean.txt](data/Costituzione_ITALIANO_clean.txt). The text is mostly clean, although some words were incorrectly split (e.g., "cattolica" might appear as "ca ttolica").

## Correcting Split Words with LLM
Initial attempts using simpler models like GPT-2 did not yield the desired results. I then tested models that are efficient and suitable for the task.

Using [Llama_3_1_8B_correct_split_words.ipynb](Llama_3_1_8B_correct_split_words.ipynb), I evaluated the `Meta Llama 3.1 8B` model for correcting split words. Running the inference on a Colab T4 GPU, which lacked sufficient memory, required a meta device, leading to a few minutes of processing time per case. By comparison, using the Lamini API with the same model reduced the inference time to just a few seconds.

Further tests revealed that `GPT-4 mini` performed comparably to `Llama 3.1 8B`. Given the low cost of serverless inference APIs (approximately a few cents for 80,000 characters or 20,000 tokens based on OpenAI's 4-character-per-token estimate), I opted for this model.

With [make_cleaner_correct_split_words.py](make_cleaner_correct_split_words.py), I processed each "Art." section using OpenAI’s `GPT-4 mini` to correct split words, resulting in a near-perfect text version, saved as [Costituzione_ITALIANO_cleaner.txt](data/Costituzione_ITALIANO_cleaner.txt). The total cost was minimal, as expected.

## Entity Extraction with Regular Expressions
I used [re_find_entities.py](re_find_entities.py) to extract entities using regular expressions, saving the results in [re_entities.json](data/re_entities.json). This method identified **211 entities**.

## Entity Extraction with Named Entity Recognition (NER)
Using [ner_find_entities.py](ner_find_entities.py), I applied spaCy’s NER model to extract entities. The results were saved in [ner_entities.json](data/ner_entities.json). This approach, leveraging NLP techniques, was more reliable than regular expressions, identifying **234 entities** in total.

## Bonus: Extracting Regulatory References
### Dirty PDF to Text Conversion
With [make_dirty_pdf2txt.py](make_dirty_pdf2txt.py), I converted the entire PDF (including footnotes) into text, fixing words split by hyphens across lines and making other minor corrections.

### Extracting Regulatory References with Regular Expressions
Finally, I used [re_find_regulatory_references.py](re_find_regulatory_references.py) to identify regulatory references in the Italian Constitution through regular expressions, saving the results to [regulatory_references.json](data/regulatory_references.json). A total of **41 references** were found.