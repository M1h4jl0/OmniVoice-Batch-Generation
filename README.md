# 🎙️ OmniVoice Batch Generation GUI

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Framework](https://img.shields.io/badge/UI-Tkinter-orange.svg)](https://docs.python.org/3/library/tkinter.html)

A clean, desktop application designed to batch-process structured slide scripts into localized, high-quality audio narration files. Powered by the **OmniVoice** model, it uses advanced voice cloning to synthesize natural speech across multiple text segments automatically.

---

## ✨ Features

* **📦 Batch Processing:** Automatically splits source text files using a custom delimiter (`---`) to generate distinct audio tracks for separate slides or modules.
* **🗣️ Voice Cloning Engine:** Leverages `OmniVoice` neural architecture to clone a voice sample accurately using a clean reference `.wav` file and text prompt.
* **⚡ Hardware Acceleration:** Detects and runs natively on NVIDIA GPUs via **CUDA** or Apple Silicon via **MPS** for lightning-fast synthesis, falling back gracefully to CPU when necessary.
* **🖥️ Responsive UI:** Features a native, responsive desktop layout built with Tkinter that stays active on a background thread—ensuring your window never freezes or displays "(Not Responding)" mid-generation.

---

## 🛠️ How It Works

The application architecture cleanly separates the user configuration panel from the background execution worker:



1. **Text Parsing:** The text file is scanned and split into isolated strings wherever the `---` divider is found.
2. **Model Loading:** PyTorch checks your hardware assets and loads the `k2-fsa/OmniVoice` weights directly into memory.
3. **Audio Generation:** The model steps through each slide text entry sequentially, referencing your source `.wav` voice properties, and saves individual files (`audio1.wav`, `audio2.wav`, etc.) directly into your target directory.

---

## 🚀 Getting Started (Source Installation)

If you want to run the application from the Python source code, ensure you have your virtual environment configured properly.

### 1. Clone the Repository
```bash
git clone [https://github.com/M1h4jl0/OmniVoice-Batch-Generation.git](https://github.com/M1h4jl0/OmniVoice-Batch-Generation.git)
cd OmniVoice-Batch-Generation
```

### 2. Set Up Your Virtual Environment
It is highly recommended to use an isolated environment to prevent version conflicts with your global libraries:

```bash
# Create the environment
python -m venv venv

# Activate it (Windows Command Prompt)
venv\Scripts\activate

# Activate it (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### 3. Install GPU-Accelerated Dependencies
Because OmniVoice relies on heavy neural network processing, you need the CUDA-enabled version of PyTorch to run generation tasks on your graphics card instead of your CPU:

```bash
# Install core audio processing and voice libraries
pip install soundfile omnivoice

# Install PyTorch with native CUDA 12.1 support
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121) --force-reinstall
```
### 4. Run the Application
Once the dependencies are successfully built inside your environment, boot up the interface:

```bash
python app.py
```

## 📖 How to Use the Software

* **Output Directory:** Click *Browse...* and select the destination folder where you want your generated audio files saved.
* **Select Slide Text File:** Choose the `.txt` document containing your narration scripts. Ensure different segments are cleanly divided by a line containing only `---`.
* **Select Reference Voice Sample:** Choose a short, clean, noise-free `.wav` audio file of the voice you intend to clone.
* **Reference Audio Text:** Paste the exact text spoken in your reference audio sample into the text box. This aligns the neural network's phonetic dictionary.
* **Generate:** Click **Translate & Generate Audio**. Keep an eye on your command line terminal to monitor initialization and GPU utilization metrics!

## 💾 Looking for the Desktop Executable?

If you prefer a plug-and-play desktop application without setting up a development workspace, head over to the **Releases** tab on the right side of this page.

Download the zipped distribution file, unpack it completely to your hard drive, and launch **`app.exe`** directly!
