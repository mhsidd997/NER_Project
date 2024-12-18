import spacy
import fitz  # PyMuPDF
from transformers import pipeline

# Load spaCy's NER model
nlp = spacy.load("en_core_web_sm")

# Load a text generation model (e.g., GPT-2)
generator = pipeline("text-generation", model="gpt2")

def extract_entities(text):
    """Extract entities using spaCy."""
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})
    return entities

def generate_sentences(entities):
    """Generate meaningful sentences from extracted entities."""
    # Prepare prompt for the generative model
    entity_texts = [entity["text"] for entity in entities]
    prompt = f"Create a meaningful sentence using the following entities: {', '.join(entity_texts)}."
    
    # Use GPT to generate text
    response = generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"]

def process_text(text):
    """Process plain text: Extract entities and generate sentences."""
    entities = extract_entities(text)
    if entities:
        generated_sentence = generate_sentences(entities)
        return {"entities": entities, "generated_sentence": generated_sentence}
    return {"entities": [], "generated_sentence": "No entities found."}

def process_pdf(pdf_path):
    """Process a PDF file: Extract text, entities, and generate sentences."""
    with fitz.open(pdf_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    
    return process_text(text)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="NER and Sentence Generation")
    parser.add_argument("--text", type=str, help="Input plain text.")
    parser.add_argument("--pdf", type=str, help="Path to input PDF file.")
    args = parser.parse_args()

    if args.text:
        result = process_text(args.text)
        print("Extracted Entities:", result["entities"])
        print("Generated Sentence:", result["generated_sentence"])
    elif args.pdf:
        result = process_pdf(args.pdf)
        print("Extracted Entities:", result["entities"])
        print("Generated Sentence:", result["generated_sentence"])
    else:
        print("Please provide input text or a PDF file.")