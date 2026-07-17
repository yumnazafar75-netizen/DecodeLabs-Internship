import unittest
from pathlib import Path

from recommender import load_roles, parse_skills, recommend


DATASET = Path(__file__).with_name("raw_skills.csv")


class RecommenderTests(unittest.TestCase):
    def setUp(self):
        self.roles = load_roles(DATASET)

    def test_aliases_are_normalized_and_deduplicated(self):
        self.assertEqual(parse_skills("Python, ML, machine learning, K8s"), ["python", "machine learning", "kubernetes"])

    def test_cloud_profile_prefers_devops_or_cloud_engineering(self):
        result = recommend("Cloud Computing, Docker, Kubernetes, CI/CD", self.roles)
        self.assertIn(result[0].role, {"DevOps Engineer", "Cloud Engineer"})
        self.assertGreater(result[0].score, result[-1].score)

    def test_requires_three_distinct_skills(self):
        with self.assertRaisesRegex(ValueError, "at least three"):
            recommend("Python, Python, SQL", self.roles)


if __name__ == "__main__":
    unittest.main()
