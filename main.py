import re
import json
import spacy
from spacy.tokens import Span
from spacy.language import Language

@Language.component("find_custom_entities")
def find_custom_entities(doc):
    custom_entities = {
        "CAMERA": ["camera", "camera dei deputati"],
        "SENATO": ["senato", "senato della repubblica"],
        "PRESIDENTE": ["presidente della repubblica"],
        "GOVERNO": ["governo"],
        "REGIONE": ["regione"],
        "PARLAMENTO": ["parlamento"],
        "CSM": ["consiglio superiore della magistratura"],
        "CONSIGLIO": ["consiglio"],
    }
    
    new_ents = []
    for label, patterns in custom_entities.items():
        for pattern in patterns:
            for match in re.finditer(pattern, doc.text, re.IGNORECASE):
                start, end = match.span()
                span = doc.char_span(start, end, label=label)
                if span is not None:
                    new_ents.append(span)
    doc.ents = list(doc.ents) + new_ents
    return doc

def create_custom_ner():
    nlp = spacy.load("it_core_news_sm")
    nlp.add_pipe("find_custom_entities", last=True)
    return nlp

def preprocess_text(text):
    # Join lines that don't end with sentence-ending punctuation
    lines = text.split('\n')
    processed_lines = []
    current_line = ""
    for line in lines:
        if current_line:
            current_line += " "
        current_line += line.strip()
        if current_line.endswith(('.', '?', '!')):
            processed_lines.append(current_line)
            current_line = ""
    if current_line:  # Add any remaining text
        processed_lines.append(current_line)
    
    return ' '.join(processed_lines)

def extract_entities_ner(text):
    nlp = create_custom_ner()
    doc = nlp(text)
    
    entities = []
    for ent in doc.ents:
        entities.append({
            'iri': ent.label_.lower(),
            'label': ent.text,
            'span_start': ent.start_char,
            'span_end': ent.end_char,
            'method': 'ner'
        })
    
    return entities

def extract_entities_regex(text):
    entities = []
    patterns = [
        (r'\b(Camera|Camera\s+dei\s+Deputati)\b', 'camera'),
        (r'\b(Senato|Senato\s+della\s+Repubblica)\b', 'senato'),
        (r'\b(Presidente\s+della\s+Repubblica)\b', 'presidente'),
        (r'\b(Governo)\b', 'governo'),
        (r'\b(Regione)\b', 'regione'),
        (r'\b(Parlamento)\b', 'parlamento'),
        (r'\b(Consiglio\s+superiore\s+della\s+magistratura)\b', 'csm'),
        (r'\b(Consiglio)\b', 'consiglio'),
        (r'\b(l\.\s*cost\.\s*\d{1,2}\s+\w+\s+\d{4},\s*n\.\s*\d+)', 'legal_ref')
    ]
    
    for pattern, iri in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            entities.append({
                'iri': iri,
                'label': match.group(0),
                'span_start': match.start(),
                'span_end': match.end(),
                'method': 'regex'
            })
    
    return entities

def compare_results(ner_entities, regex_entities):
    all_entities = ner_entities + regex_entities
    all_entities.sort(key=lambda x: (x['span_start'], x['span_end']))
    
    comparison = []
    for entity in all_entities:
        existing = next((e for e in comparison if e['span_start'] == entity['span_start'] and e['span_end'] == entity['span_end']), None)
        if existing:
            existing['methods'].append(entity['method'])
        else:
            comparison.append({**entity, 'methods': [entity['method']]})
    
    return comparison

def main():
    with open('costituzione_italiana.txt', 'r', encoding='utf-8') as file:
        raw_text = file.read()
    
    preprocessed_text = preprocess_text(raw_text)
    
    ner_entities = extract_entities_ner(preprocessed_text)
    regex_entities = extract_entities_regex(preprocessed_text)
    
    comparison = compare_results(ner_entities, regex_entities)
    
    with open('entities_comparison.json', 'w', encoding='utf-8') as outfile:
        json.dump(comparison, outfile, ensure_ascii=False, indent=2)
    
    # Print summary
    ner_only = sum(1 for e in comparison if e['methods'] == ['ner'])
    regex_only = sum(1 for e in comparison if e['methods'] == ['regex'])
    both = sum(1 for e in comparison if set(e['methods']) == {'ner', 'regex'})
    
    print(f"Entities found by NER only: {ner_only}")
    print(f"Entities found by Regex only: {regex_only}")
    print(f"Entities found by both methods: {both}")

    # Print entities found by each method
    print("\nEntities found only by NER:")
    for entity in comparison:
        if entity['methods'] == ['ner']:
            print(f"- {entity['label']} ({entity['iri']})")

    print("\nEntities found only by Regex:")
    for entity in comparison:
        if entity['methods'] == ['regex']:
            print(f"- {entity['label']} ({entity['iri']})")

    print("\nEntities found by both methods:")
    for entity in comparison:
        if set(entity['methods']) == {'ner', 'regex'}:
            print(f"- {entity['label']} ({entity['iri']})")

if __name__ == "__main__":
    main()