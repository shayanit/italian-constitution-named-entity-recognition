import json
from itertools import islice


def load_entities(file_path):
    """Load entities from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_entities(entities_1, entities_2):
    """Compare two lists of entities and return common and unique ones."""
    set_1 = {(ent['label'], ent['span_start'], ent['span_end']) for ent in entities_1}
    set_2 = {(ent['label'], ent['span_start'], ent['span_end']) for ent in entities_2}
    
    # Find common entities
    common = set_1 & set_2
    
    # Find unique entities
    unique_to_script1 = set_1 - set_2
    unique_to_script2 = set_2 - set_1
    
    return common, unique_to_script1, unique_to_script2

import re

def get_sentence(text, span_start, span_end):
    """Extract the sentence containing the entity."""
    # Get the entity's substring from the text
    entity_text = text[span_start:span_end]
    
    # Find the sentence boundaries by looking for the closest punctuation before and after the entity
    start_of_sentence = text.rfind('.', 0, span_start)  # Find the last period before the entity
    end_of_sentence = text.find('.', span_end)          # Find the next period after the entity
    
    # If no period is found, assume the start or end of the text
    if start_of_sentence == -1:
        start_of_sentence = 0
    else:
        start_of_sentence += 1  # Move start to just after the period
    
    if end_of_sentence == -1:
        end_of_sentence = len(text)
    
    # Return the sentence, strip leading/trailing whitespaces
    sentence = text[start_of_sentence:end_of_sentence].strip()
    
    return sentence

def print_entity_with_sentence(entities, text):
    """Print each entity with the sentence it was found in."""
    for entity in entities:
        sentence = get_sentence(text, entity[1], entity[2])
        print(f"Entity: {entity[0]}")
        print(f"Sentence: {sentence}")
        print('-' * 50)

def main():
    # Load entities from both scripts
    entities_regex = load_entities('re_entities.json')
    entities_spacy = load_entities('ner_entities.json')

    # Compare entities
    common, unique_to_regex, unique_to_spacy = compare_entities(entities_regex, entities_spacy)

    # Print results
    print(f"Common entities found: {len(common)}")
    for entity in common:
        print(f"  - {entity}")

    print(f"\nEntities found only by the regex script: {len(unique_to_regex)}")
    for entity in unique_to_regex:
        print(f"  - {entity}")

    print(f"\nEntities found only by the spaCy script: {len(unique_to_spacy)}")
    for entity in unique_to_spacy:
        print(f"  - {entity}")
    
    
    text = ""
    with open("Costituzione_ITALIANO_clean.txt", 'r', encoding='utf-8') as f:
        text = f.read()
    
    n=5
    
    print(f"Sentences related to the first {n} entities that were only found by regex:")
    entities_to_print = list(islice(unique_to_regex, 5))
    print(print_entity_with_sentence(entities_to_print, text))
    

    print(f"Sentences related to the first {n} entities that were only found by NER:")
    print(print_entity_with_sentence(islice(unique_to_spacy, 5), text))

# Call the main function
main()
