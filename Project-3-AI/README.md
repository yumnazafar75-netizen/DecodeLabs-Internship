# Tech Stack Recommender

This is a content-based recommendation system for the Project 3 capstone. It maps a user's skills to job roles, applies TF-IDF weighting, calculates cosine similarity, and displays the top three career paths.

## Run

From this folder, run:

```powershell
python recommender.py
```

Example input:

```text
Python, SQL, Machine Learning, Data Visualization
```

## Test

```powershell
python -m unittest -v
```

## How it meets the assignment

- Input: requires at least three distinct skills.
- Process: normalizes skills, applies smoothed TF-IDF, then computes cosine similarity.
- Output: sorts all job roles and returns the top three with a match percentage and matched skills.
- Cold start: the required initial skills provide the onboarding profile needed to make recommendations.

The dataset is deliberately simple and editable. Add more roles and comma-separated skills to `raw_skills.csv` without changing the algorithm.
