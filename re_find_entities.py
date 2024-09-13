import re
import json

# Define the entities and their patterns
entity_patterns = {
    "camera_deputati": r"(Camera|Camera dei Deputati)",
    "senato_repubblica": r"(Senato|Senato della Repubblica)",
    "presidente_repubblica": r"Presidente della Repubblica",
    "governo": r"Governo",
    "regione": r"Regione",
    "parlamento": r"Parlamento",
    "consiglio_superiore_magistratura": r"Consiglio superiore della magistratura",
    "consiglio": r"Consiglio"
}

def extract_entities(text):
    entities = []
    
    # Iterate over each pattern and find matches
    for iri, pattern in entity_patterns.items():
        for match in re.finditer(pattern, text):
            entity = {
                "iri": iri,
                "label": match.group(),
                "span_start": match.start(),
                "span_end": match.end()
            }
            entities.append(entity)
    
    return entities

def main(input_file, output_file):
    # Read the cleaned text
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Extract entities
    entities = extract_entities(text)

    # Save the entities to a JSON file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(entities, f_out, ensure_ascii=False, indent=4)

    print(f"{len(entities)} entities have been successfully extracted and saved to {output_file}")

# Call the main function
main('data/Costituzione_ITALIANO_cleaner.txt', 'data/re_entities.json')
