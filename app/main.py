from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.models import (
    CompanyInput,
    Profile,
    ProfileCreateRequest,
    ProfilePatchRequest,
)
from app.services.ppt import compose_ppt
from app.services.validation import validate_profile
from app.store import store

app = FastAPI(title="AI Company Profile Tool")
EXPORT_DIR = Path("exports")


class ExportResponse(BaseModel):
    profile_id: UUID
    path: str


@app.post("/profiles", response_model=Profile)
def create_profile(payload: ProfileCreateRequest) -> Profile:
    profile = Profile(profile_type=payload.profile_type, company_input=CompanyInput(name=payload.company_name))
    return store.create(profile)


@app.get("/profiles/{profile_id}", response_model=Profile)
def get_profile(profile_id: UUID) -> Profile:
    try:
        return store.get(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Profile not found") from exc


@app.patch("/profiles/{profile_id}/fields", response_model=Profile)
def patch_profile(profile_id: UUID, payload: ProfilePatchRequest) -> Profile:
    try:
        profile = store.get(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Profile not found") from exc

    for dotted_key, value in payload.fields.items():
        parts = dotted_key.split(".")
        node: Any = profile
        for part in parts[:-1]:
            node = getattr(node, part)
        setattr(node, parts[-1], value)

    errors = validate_profile(profile)
    profile.quality.conflicts = errors
    return store.update(profile)


@app.post("/profiles/{profile_id}/export/pptx", response_model=ExportResponse)
def export_profile(profile_id: UUID) -> ExportResponse:
    try:
        profile = store.get(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Profile not found") from exc

    output = compose_ppt(profile, EXPORT_DIR)
    profile.exported_pptx_path = str(output)
    store.update(profile)
    return ExportResponse(profile_id=profile_id, path=str(output))


@app.get("/profiles/{profile_id}/download/pptx")
def get_export(profile_id: UUID) -> dict[str, str]:
    try:
        profile = store.get(profile_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Profile not found") from exc

    if not profile.exported_pptx_path:
        raise HTTPException(status_code=404, detail="No export available")

    return {"path": profile.exported_pptx_path}
