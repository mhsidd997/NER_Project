import sys
import spacy
import json
import argparse
import fitz

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to process text and extract NER sentences
def process_text(input_text):
    doc = nlp(input_text)
    sentences_with_entities = []

    for sent in doc.sents:
        entities = [{"text": ent.text, "label": ent.label_} for ent in sent.ents]
        if entities:
            sentences_with_entities.append({"sentence": sent.text, "entities": entities})
    
    return sentences_with_entities

# Function to process PDF and extract text
def process_pdf(pdf_path):
    pdf_text = ""
    pdf_document = fitz.open(pdf_path)
    for page in pdf_document:
        pdf_text += page.get_text()
    return process_text(pdf_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", help="Path to PDF file", type=str, default=None)
    parser.add_argument("text", nargs='?', help="Input text for NER", default=None)

    args = parser.parse_args()

    if args.pdf:
        result = process_pdf(args.pdf)
    elif args.text:
        result = process_text(args.text)
    else:
        result = {"error": "No input provided"}

    print(json.dumps(result))