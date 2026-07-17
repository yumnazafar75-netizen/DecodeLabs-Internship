"""A dependency-free TF-IDF and cosine-similarity tech role recommender."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


# The aliases let natural user input map to the vocabulary used by the dataset.
ALIASES = {
    "amazon web services": "aws",
    "aws cloud": "aws",
    "cloud computing": "cloud",
    "continuous integration": "ci/cd",
    "continuous delivery": "ci/cd",
    "continuous integration/continuous delivery": "ci/cd",
    "k8s": "kubernetes",
    "machine learning": "machine learning",
    "ml": "machine learning",
    "application programming interfaces": "rest apis",
    "api": "rest apis",
    "apis": "rest apis",
    "database": "databases",
    "data visualization": "data visualization",
}


@dataclass(frozen=True)
class Recommendation:
    role: str
    score: float
    matched_skills: tuple[str, ...]


def normalize_skill(skill: str) -> str:
    """Normalize a skill string and translate common aliases."""
    cleaned = re.sub(r"\s+", " ", skill.strip().casefold())
    return ALIASES.get(cleaned, cleaned)


def parse_skills(skills: str | Iterable[str]) -> list[str]:
    """Return unique, normalized skills while keeping their input order."""
    raw = skills.split(",") if isinstance(skills, str) else skills
    result: list[str] = []
    for skill in raw:
        normalized = normalize_skill(skill)
        if normalized and normalized not in result:
            result.append(normalized)
    return result


def load_roles(csv_path: str | Path) -> dict[str, list[str]]:
    """Load job-role documents from the assignment dataset format."""
    with Path(csv_path).open(encoding="utf-8", newline="") as file:
        rows = csv.DictReader(file)
        if not rows.fieldnames or not {"role", "skills"}.issubset(rows.fieldnames):
            raise ValueError("CSV must have 'role' and 'skills' columns.")
        roles = {row["role"].strip(): parse_skills(row["skills"]) for row in rows}
    if not roles:
        raise ValueError("The role dataset is empty.")
    return roles


def idf(documents: Iterable[Iterable[str]]) -> dict[str, float]:
    """Calculate smoothed inverse-document-frequency values for each skill."""
    docs = [set(document) for document in documents]
    count = len(docs)
    frequencies = Counter(skill for document in docs for skill in document)
    # Smoothed IDF avoids a zero value for skills present in every role.
    return {skill: math.log((1 + count) / (1 + frequency)) + 1 for skill, frequency in frequencies.items()}


def tfidf_vector(skills: Iterable[str], weights: dict[str, float]) -> dict[str, float]:
    counts = Counter(skills)
    total = sum(counts.values())
    if not total:
        return {}
    return {skill: (count / total) * weights.get(skill, 0.0) for skill, count in counts.items() if skill in weights}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    dot_product = sum(value * right.get(skill, 0.0) for skill, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot_product / (left_norm * right_norm) if left_norm and right_norm else 0.0


def recommend(user_skills: str | Iterable[str], roles: dict[str, list[str]], top_n: int = 3) -> list[Recommendation]:
    """Rank roles by TF-IDF weighted cosine similarity to the user's skills."""
    user = parse_skills(user_skills)
    if len(user) < 3:
        raise ValueError("Please provide at least three distinct skills, separated by commas.")
    if top_n < 1:
        raise ValueError("top_n must be at least 1.")

    weights = idf([*roles.values(), user])
    user_vector = tfidf_vector(user, weights)
    recommendations = []
    for role, role_skills in roles.items():
        score = cosine_similarity(user_vector, tfidf_vector(role_skills, weights))
        matches = tuple(skill for skill in user if skill in role_skills)
        recommendations.append(Recommendation(role, score, matches))
    return sorted(recommendations, key=lambda item: (-item.score, item.role))[:top_n]


def main() -> None:
    dataset = Path(__file__).with_name("raw_skills.csv")
    roles = load_roles(dataset)
    print("Tech Stack Recommender")
    print("Enter at least three skills separated by commas (e.g. Python, SQL, Cloud).")
    user_skills = input("> ")
    try:
        results = recommend(user_skills, roles)
    except ValueError as error:
        print(f"Input error: {error}")
        return

    print("\nTop career-path matches:")
    for rank, item in enumerate(results, start=1):
        matched = ", ".join(item.matched_skills) if item.matched_skills else "no direct dataset matches"
        print(f"{rank}. {item.role} - {item.score:.1%} match (matched: {matched})")


if __name__ == "__main__":
    main()
