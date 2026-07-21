# Project 4 - OCR Recognition Pipeline

This implementation follows the project brief's OCR path. It uses EasyOCR's pre-trained recognition model, performs grayscale conversion, Gaussian blur, adaptive thresholding, filters words below 80% confidence, and produces visual bounding boxes. No separate OCR application is needed.

## Setup

Install Python packages:

```powershell
python -m pip install -r requirements.txt
```

EasyOCR downloads its pre-trained model automatically the first time you run the script. Keep an internet connection available for that first run.

## Run

```powershell
python recognize.py --input path\to\image.jpg --output outputs --min-confidence 80
```

For another language, add its EasyOCR code; for example: `--languages en hi`.

## Deliverables

The output folder contains:

- `preprocessed.png` - proof of grayscale/blur/adaptive-threshold preprocessing.
- `annotated.png` - original image with labeled word bounding boxes.
- `recognized.txt` - accepted extracted text.
- `words.csv` - text, confidence, and bounding-box coordinates.

For the milestone validation, submit the script, one sample input, and these four generated files. Use an input where several clearly visible words score at least 80%.
