# AI-Generated Company Profile Tool (M&A)

This repository provides a starter implementation for generating one-slide, PPTX-ready company profiles from a company name.

## Included in this baseline

- FastAPI endpoints for profile create/read/edit/export.
- Canonical JSON profile model with evidence objects.
- Deterministic ownership fallback engine implementing rules 1-4 exactly.
- Validation checks aligned to acceptance criteria (citations, ownership rule range, narrative citations).
- PPTX composer that writes editable text into named shapes matching the template contract.

## API

- `POST /profiles`
- `GET /profiles/{id}`
- `PATCH /profiles/{id}/fields`
- `POST /profiles/{id}/export/pptx`
- `GET /profiles/{id}/download/pptx`

## Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Tests

```bash
pytest -q
```
