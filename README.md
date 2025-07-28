# Adobe Hackathon Project - Round 1 (1A & 1B)

This repository includes solutions to **Adobe India Hackathon Round 1**, consisting of two parts:

- **Challenge 1A**: Extracting titles and heading outlines from PDF files.
- **Challenge 1B**: Ranking relevant sections based on persona and job descriptions using semantic search.

---

## Folder Structure

```bash
.
├── extractor.py                # Solution for Challenge 1A
├── ranker.py                   # Solution for Challenge 1B
├── Dockerfile                  # Dockerfile to containerize the project
├── requirements.txt            # Python dependencies
├── input/                      # Input PDF files for Challenge 1A
│   └── sample.pdf              # Example input PDF
├── output/                     # Output folder for extractor (1A)
│   └── sample.json             # Generated JSON after extractor
├── round_ib/
│   ├── input/
│   │   └── challenge_1b.json   # Input JSON for Challenge 1B
│   └── ouput/                  # Output folder for Challenge 1B result
```

---

## Requirements

Ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (Windows/Linux/macOS)

---

## Step-by-Step Instructions

### Step 1: Clone or Download Project

Place all files (`extractor.py`, `ranker.py`, `Dockerfile`, etc.) in a single project folder.

---

### Step 2: Place Your PDF File

Put your input PDF into the `/input` directory. Example:

```
input/sample.pdf
```

---

### Step 3: Build Docker Image

Run the following command in PowerShell (from project root):

```powershell
docker build --platform linux/amd64 -t mysolution:latest .
```

This will:

- Use Python 3.10 base image
- Install dependencies like PyMuPDF, torch, sentence-transformers
- Cache the model from HuggingFace (if online)

---

### Step 4: Run Challenge 1A (extractor.py)

Extract headings and title from the PDF:

```powershell
docker run --rm `
  -v "${PWD}/input:/app/input" `
  -v "${PWD}/output:/app/output" `
  mysolution:latest python extractor.py
```

✅ Output: `output/sample.json`

---

Outer Input and output folder are for Round 1A
round_ib Input and output folder are for Round 1B

### Step 5: Prepare for Challenge 1B (ranker.py)

1. Move the `sample.json` generated above into:

   ```
   round_ib/input/sample.json
   ```

2. Create and edit your `challenge_1b.json` in:

   ```
   round_ib/input/challenge_1b.json
   ```

   Example format:

   ```json
   {
     "challenge_info": {
       "challenge_id": "round_1b_local_gov_001",
       "test_case_name": "gov_ops",
       "description": "Policy extraction"
     },
     "documents": [
       {
         "filename": "sample.pdf",
         "title": "Policy Document"
       }
     ],
     "persona": {
       "role": "Government Administrative Officer"
     },
     "job_to_be_done": {
       "task": "Extract policy sections and summarize actionable rules."
     }
   }
   ```

---

### Step 6: Run Challenge 1B (ranker.py)

Run the following:

```powershell
docker run --rm `
  -v "${PWD}/round_ib/input:/app/round_ib/input" `
  -v "${PWD}/round_ib/ouput:/app/round_ib/ouput" `
  mysolution:latest python ranker.py
```

✅ Output: `round_ib/ouput/ranked.json`

---

## Troubleshooting

- **Model Download Issues**:

  - Ensure Docker has internet access (remove `--network none`)
  - Avoid `--network=none` for the first model load

- **NumPy Error**:

  - Ensure version is `< 2.0` or use: `numpy==1.24.4` in `requirements.txt`

---

## Requirements.txt (cleaned)

```txt
PyMuPDF==1.23.6
torch==2.0.1
sentence-transformers==2.2.2
numpy==1.24.4
```

---

---

## Credits

- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Sentence-Transformers](https://www.sbert.net/)
- [PyTorch](https://pytorch.org/)
- [Docker](https://www.docker.com/)

---

Feel free to modify or extend this project as per your hackathon needs!

```
```
