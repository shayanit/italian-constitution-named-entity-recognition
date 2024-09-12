import spacy
import json

# Load the small Italian model
nlp = spacy.load('it_core_news_sm')

# Define a set of administrative entity keywords that you want to capture
administrative_entities = {
    "camera_deputati": ["Camera", "Camera dei Deputati"],
    "senato_repubblica": ["Senato", "Senato della Repubblica"],
    "presidente_repubblica": ["Presidente della Repubblica"],
    "governo": ["Governo"],
    "regione": ["Regione"],
    "parlamento": ["Parlamento"],
    "consiglio_superiore_magistratura": ["Consiglio superiore della magistratura"],
    "consiglio": ["Consiglio"]
}

def extract_entities_spacy(text):
    doc = nlp(text)
    entities = []

    # Iterate through sentences and search for our administrative entities
    for ent in doc.ents:
        for iri, entity_list in administrative_entities.items():
            for entity in entity_list:
                if entity.lower() in ent.text.lower():  # Case-insensitive match
                    entity_data = {
                        "iri": iri,
                        "label": ent.text,
                        "span_start": ent.start_char,
                        "span_end": ent.end_char
                    }
                    entities.append(entity_data)

    return entities

def main(input_file, output_file):
    # Read the cleaned text
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract entities using spaCy
    entities = extract_entities_spacy(text)

    # Save the entities to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(entities, f_out, ensure_ascii=False, indent=4)

    print(f"Entities have been successfully extracted using spaCy and saved to {output_file}")

# Call the main function
main('Costituzione_ITALIANO_clean.txt', 'ner_entities.json')
