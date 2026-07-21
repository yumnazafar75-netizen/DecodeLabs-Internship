"""OCR pipeline for DecodeLabs Project 4 using EasyOCR.

Example:
    python recognize.py --input samples/receipt.jpg --output outputs --min-confidence 80
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import cv2
import easyocr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract high-confidence text and save an annotated image."
    )
    parser.add_argument("--input", required=True, type=Path, help="Image to recognize")
    parser.add_argument("--output", default=Path("outputs"), type=Path, help="Result folder")
    parser.add_argument(
        "--min-confidence", type=float, default=80.0,
        help="Keep words at or above this confidence (default: 80)",
    )
    parser.add_argument(
        "--languages", nargs="+", default=["en"],
        help="EasyOCR language codes (default: en)",
    )
    return parser.parse_args()


def preprocess(image):
    """Convert BGR input into a clean binary image for OCR."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )


def extract_words(binary_image, languages, minimum_confidence: float):
    """Return only non-empty OCR words passing the requested confidence gate."""
    reader = easyocr.Reader(languages, gpu=False)
    results = reader.readtext(binary_image, detail=1, paragraph=False)
    words = []
    for box, raw_text, raw_confidence in results:
        text = raw_text.strip()
        confidence = float(raw_confidence) * 100
        if text and confidence >= minimum_confidence:
            points = [(int(x), int(y)) for x, y in box]
            x_values, y_values = zip(*points)
            left, top = min(x_values), min(y_values)
            words.append(
                {
                    "text": text,
                    "confidence": round(confidence, 2),
                    "left": left,
                    "top": top,
                    "width": max(x_values) - left,
                    "height": max(y_values) - top,
                }
            )
    return words


def draw_words(image, words):
    annotated = image.copy()
    for word in words:
        x, y, w, h = word["left"], word["top"], word["width"], word["height"]
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 180, 0), 2)
        label = f'{word["text"]} ({word["confidence"]:.0f}%)'
        cv2.putText(
            annotated, label, (x, max(18, y - 6)), cv2.FONT_HERSHEY_SIMPLEX,
            0.5, (0, 120, 0), 1, cv2.LINE_AA,
        )
    return annotated


def save_results(output_dir: Path, binary_image, annotated_image, words) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_dir / "preprocessed.png"), binary_image)
    cv2.imwrite(str(output_dir / "annotated.png"), annotated_image)
    (output_dir / "recognized.txt").write_text(
        " ".join(word["text"] for word in words) + "\n", encoding="utf-8"
    )
    with (output_dir / "words.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "confidence", "left", "top", "width", "height"])
        writer.writeheader()
        writer.writerows(words)


def main() -> int:
    args = parse_args()
    if not 0 <= args.min_confidence <= 100:
        print("--min-confidence must be between 0 and 100.", file=sys.stderr)
        return 2
    if not args.input.is_file():
        print(f"Input image not found: {args.input}", file=sys.stderr)
        return 2

    image = cv2.imread(str(args.input))
    if image is None:
        print("The input is not a readable image.", file=sys.stderr)
        return 2
    binary = preprocess(image)
    words = extract_words(binary, args.languages, args.min_confidence)

    save_results(args.output, binary, draw_words(image, words), words)
    print(f"Recognized {len(words)} words at >= {args.min_confidence:.0f}% confidence.")
    print(f"Saved results to: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
