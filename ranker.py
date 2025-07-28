import os
import json
from pathlib import Path
from datetime import datetime
import torch
from sentence_transformers import SentenceTransformer, util


INPUT_FILE = "round_ib/input/challange_1b.json"
INPUT_DIR = "round_ib/input"
OUTPUT_FILE = "round_ib/ouput/ranked.json"
TOP_K = 5
MODEL_NAME = "all-MiniLM-L6-v2"

# Load challenge_ib.json
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    challenge_data = json.load(f)

documents = challenge_data["documents"]
persona = challenge_data["persona"]["role"]
job_task = challenge_data["job_to_be_done"]["task"]
query_text = persona + ". " + job_task


model = SentenceTransformer(MODEL_NAME)

all_sections = []

for doc in documents:
    pdf_filename = doc["filename"]
    json_filename = os.path.splitext(pdf_filename)[0] + ".json"
    json_path = os.path.join(INPUT_DIR, json_filename)

    if not os.path.exists(json_path):
        print(f" Warning: JSON file for {pdf_filename} not found at {json_path}")
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        doc_data = json.load(f)

    outline = doc_data.get("outline", [])

    for entry in outline:
        level = entry.get("level", "")
        if level not in ["H1", "H2", "H3"]:
            continue

        section = {
            "document": pdf_filename,
            "section_title": entry.get("text", "").strip(),
            "page_number": entry.get("page", 0),
            "level": level,
            "raw_text": entry.get("text", "").strip()
        }

        all_sections.append(section)

print(f" Loaded {len(all_sections)} sections from {len(documents)} documents.")

# Creating embeddings of query and sections
section_texts = [s["raw_text"] for s in all_sections]
query_embedding = model.encode(query_text, convert_to_tensor=True)
section_embeddings = model.encode(section_texts, convert_to_tensor=True)

cosine_scores = util.cos_sim(query_embedding, section_embeddings)[0] #for cosine similairty calulation

top_k = min(TOP_K, len(all_sections))
top_indices = torch.topk(cosine_scores, k=top_k).indices.tolist()

output = {
    "metadata": {
        "input_documents": [doc["filename"] for doc in documents],
        "persona": persona,
        "job_to_be_done": job_task,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "subsection_analysis": []
}

rank = 1
for idx in top_indices:
    section = all_sections[idx]

    output["extracted_sections"].append({
        "document": section["document"],
        "section_title": section["section_title"],
        "importance_rank": rank,
        "page_number": section["page_number"]
    })

    output["subsection_analysis"].append({
        "document": section["document"],
        "refined_text": section["raw_text"],
        "page_number": section["page_number"]
    })

    rank += 1

os.makedirs("round_ib/ouput", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n Done! Output saved to {OUTPUT_FILE}")
