# Handwritten Dataset Collector — Team Guide

Welcome team! This guide explains how to set up, use, and sync your dataset contributions for our CNN handwritten character dataset project.

---

## 🎯 Overview & Goal

We are collecting a custom dataset of handwritten characters consisting of **36 classes** (Digits `0-9` and Uppercase Letters `A-Z`) across **6 writers** (`W01` to `W06`).

- **Image Specs:** 48×48 Grayscale PNG with anti-aliased strokes.
- **Naming Format:** `[CLASS]_[WRITER]_[SAMPLE].png` (e.g., `A_W01_001.png`).
- **Target Count:** 100 samples per class per writer (36 classes × 100 = 3,600 images per person; Total dataset = 21,600 images).

---

## 🛠️ 1. Setup & Installation

### Step 1: Clone the Repository
Open your terminal / command prompt and clone the repository:
```bash
git clone https://github.com/Conca979/CNN-from-scratch-with-Numpy.git
cd CNN
```

### Step 2: Install Dependencies
Make sure you have Python 3 installed. Install the required image library:
```bash
pip install Pillow
```

---

## 🎨 2. How to Collect Data

1. **Launch the app:**
   ```bash
   python image_generation.py
   ```
2. **Select your Writer ID:**
   - In the top bar, set **Writer ID** to your assigned ID (`W01`, `W02`, `W03`, `W04`, `W05`, or `W06`). 
   - ⚠️ *Important:* Make sure you keep your assigned Writer ID selected throughout your session.
3. **Select Target Class:**
   - Pick the character you are drawing (e.g., `0`, `1`, `A`, `B`).
4. **Draw on Canvas:**
   - Use your mouse or stylus to draw the character on the canvas.
   - The app automatically applies anti-aliased smoothing to simulate real handwriting strokes.
5. **Save & Next:**
   - Click **Save & Next** (or press the button).
   - The app automatically resamples the drawing to a 48x48 grayscale image, saves it in `dataset/<class>/`, appends metadata to `dataset/metadata_<WRITER_ID>.csv`, and automatically increments the sample counter for you.
6. **Clear:**
   - Click **Clear** if you make a mistake and want to redraw.

---

## 🔄 3. Syncing Your Work to GitHub

Because filenames include your Writer ID (`..._W01_...png`) and metadata is saved to `metadata_<WRITER_ID>.csv`, **there will be no Git merge conflicts between team members**.

Push your work to GitHub periodically (e.g., after every session or every 100 images):

```bash
# 1. Stage your dataset folder
git add dataset/

# 2. Commit your progress
git commit -m "Add handwriting samples for W0X"

# 3. Pull latest changes from team
git pull --rebase origin main

# 4. Push to GitHub
git push origin main
```

---

## ❓ FAQ & Tips
- **Where are images stored?** Inside the `dataset/` directory grouped by class folders (e.g., `dataset/A/A_W01_001.png`).
- **Can I stop and continue later?** Yes! The app automatically scans your local files and picks up at the next sample ID when you re-select your Writer ID and Class.
