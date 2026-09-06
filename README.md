# Vectorized CNN in NumPy / CuPy

A custom Convolutional Neural Network built entirely from scratch using NumPy (and optionally CuPy for GPU acceleration). This project includes a CIFAR-10 image recognizer with an interactive GUI that you can train and run locally.

---

## 🌟 Features
- **Built from Scratch:** No PyTorch, TensorFlow, or Keras. Core ML operations (convolutions, pooling, linear layers, backpropagation) are manually implemented.
- **CPU & GPU Support:** Train using standard NumPy or accelerate training drastically with CuPy.
- **Interactive GUI:** An easy-to-use Tkinter application to test the model by pasting any image from your clipboard.

---

## 🛠️ 1. Setup & Installation

### Step 1: Clone the Repository
Open your terminal or command prompt and clone the project:
```bash
git clone https://github.com/Conca979/vectorized-cnn-numpy.git
cd CNN
```

### Step 2: Install Dependencies
Make sure you have Python 3 installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
```
*(The `requirements.txt` includes `numpy` and `Pillow`).*

### Optional: GPU Setup for Faster Training
If you want to train the model on an NVIDIA GPU (highly recommended for speed), you must install `cupy`. Install the CuPy version that matches your CUDA toolkit (e.g., `cupy-cuda11x` or `cupy-cuda12x`):
```bash
pip install cupy-cuda12x
```

### Step 3: Download the Dataset (For Training Only)
If you plan to train the model yourself, you will need the CIFAR-10 dataset:
1. Download the [CIFAR-10 Python version](https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz).
2. Extract the `.tar.gz` archive.
3. Place the extracted `cifar-10-batches-py` folder directly inside the `dataset/` directory of this project.

*(Your directory structure should look like this: `dataset/cifar-10-batches-py/data_batch_1`)*

---

## 🧠 2. Training the Model

You can choose to train the model on the CPU or GPU. The GPU is significantly faster.

### Option A: CPU Training
Run the CPU training script. This uses standard NumPy.
```bash
python src/train_cifa10_cpu.py
```

### Option B: GPU Training
If you have set up CuPy, run the GPU script:
```bash
python src/train_cifa10_gpu.py
```

### Saving Weights
Once training finishes, the console will ask if you want to save the pre-trained weights:
```
Want to save the pre-trained weights? -> 'y' for yes 'n' for no - 
```
Press `y` to save. The weights will be generated and stored in the `weights/` directory (e.g., `weights/cnn_cifar10_weights_GPU.npz`).

---

## 🚀 3. Running the Demo (GUI)

Once you have the trained weights (specifically `cnn_cifar10_weights_GPU.npz`), you can run the interactive GUI demo. 

**Note:** The demo does *not* require the CIFAR-10 dataset to be downloaded. You can test the model using your own images!

1. **Launch the Demo:**
   ```bash
   python src/Demo.py
   ```
2. **How to Use the App:**
   - **📋 Paste Image:** Copy any image from your computer or web browser (e.g., right-click an image and select "Copy image"). Then click this button in the app. The image will be automatically resized to fit the model (32x32).
   - **⚡ Predict:** Click this to run the image through the neural network. The app will display the predicted class (e.g., "cat", "airplane", "dog") along with confidence percentages for all 10 classes.
