from __future__ import annotations

from typing import Dict
from uuid import UUID

from app.models import Profile


class InMemoryProfileStore:
    def __init__(self) -> None:
        self._profiles: Dict[UUID, Profile] = {}

    def create(self, profile: Profile) -> Profile:
        self._profiles[profile.profile_id] = profile
        return profile

    def get(self, profile_id: UUID) -> Profile:
        return self._profiles[profile_id]

    def update(self, profile: Profile) -> Profile:
        self._profiles[profile.profile_id] = profile
        return profile


store = InMemoryProfileStore()
