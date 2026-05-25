import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import torch
import soundfile as sf
from omnivoice import OmniVoice

class OmniVoiceTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniVoice Audio Generator")
        self.root.geometry("550x550")
        self.root.minsize(500, 500)
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ttk.Label(main_frame, text="OmniVoice Batch Generation", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 15))
        
        self.dir_path = tk.StringVar()
        self.txt_path = tk.StringVar()
        self.wav_path = tk.StringVar()
        
        self.create_file_field(
            main_frame, 
            label_text="Output Directory (OUTPUT_DIR):", 
            str_var=self.dir_path, 
            browse_command=self.browse_directory
        )
        
        self.create_file_field(
            main_frame, 
            label_text="Select Slide Text File (INPUT_FILE - .txt):", 
            str_var=self.txt_path, 
            browse_command=self.browse_txt
        )
        
        self.create_file_field(
            main_frame, 
            label_text="Select Reference Voice Sample (REF_AUDIO - .wav):", 
            str_var=self.wav_path, 
            browse_command=self.browse_wav
        )
        
        ref_text_frame = ttk.Frame(main_frame)
        ref_text_frame.pack(fill="x", pady=10)
        
        ref_label = ttk.Label(ref_text_frame, text="Reference Audio Text (REF_TEXT):", font=("Helvetica", 10))
        ref_label.pack(anchor="w", pady=(0, 2))
        
        self.ref_text_box = tk.Text(ref_text_frame, height=4, font=("Helvetica", 10), wrap="word")
        self.ref_text_box.pack(fill="x")

        default_ref_text = "Ovaj modul se fokusira na jedno od najvažnijih načela: na najbolji interes deteta. Naučićete šta to znači i kako da ga primenite u praksi. Procenjeno vreme za završetak ovog modula je do jedan sat."
        self.ref_text_box.insert("1.0", default_ref_text)
        
        style = ttk.Style()
        style.configure("Action.TButton", font=("Helvetica", 11, "bold"))
        
        self.translate_btn = ttk.Button(
            main_frame, 
            text="Translate & Generate Audio", 
            command=self.on_translate_click,
            style="Action.TButton"
        )
        self.translate_btn.pack(pady=(25, 10), ipady=8, fill="x")
        
        self.status_label = ttk.Label(main_frame, text="Ready", font=("Helvetica", 10, "italic"), foreground="gray")
        self.status_label.pack()

    def create_file_field(self, parent, label_text, str_var, browse_command):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=8)
        frame.grid_columnconfigure(0, weight=1)
        
        label = ttk.Label(frame, text=label_text, font=("Helvetica", 10))
        label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))
        
        entry = ttk.Entry(frame, textvariable=str_var, font=("Helvetica", 10))
        entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        
        btn = ttk.Button(frame, text="Browse...", command=browse_command)
        btn.grid(row=1, column=1, sticky="e")

    def browse_directory(self):
        path = filedialog.askdirectory(title="Select Output Directory")
        if path: self.dir_path.set(os.path.normpath(path))
            
    def browse_txt(self):
        path = filedialog.askopenfilename(title="Select Text File", filetypes=[("Text files", "*.txt")])
        if path: self.txt_path.set(os.path.normpath(path))
            
    def browse_wav(self):
        path = filedialog.askopenfilename(title="Select WAV Audio File", filetypes=[("WAV files", "*.wav")])
        if path: self.wav_path.set(os.path.normpath(path))

    def on_translate_click(self):
        """Validates inputs and launches the script on a background thread."""
        input_file = self.txt_path.get()
        output_dir = self.dir_path.get()
        ref_audio = self.wav_path.get()
        ref_text = self.ref_text_box.get("1.0", "end-1c").strip()
        
        if not input_file or not output_dir or not ref_audio or not ref_text:
            messagebox.showwarning("Missing Fields", "Please populate all fields and provide reference text.")
            return
            
        if not os.path.exists(input_file):
            messagebox.showerror("Error", f"Input file text file not found at:\n{input_file}")
            return
            
        if not os.path.exists(ref_audio):
            messagebox.showerror("Error", f"Reference voice file (.wav) not found at:\n{ref_audio}")
            return

        self.translate_btn.config(state="disabled")
        self.status_label.config(text="Initializing OmniVoice model... Check your terminal for logs.", foreground="blue")
        
        threading.Thread(
            target=self.run_generation_backend, 
            args=(input_file, output_dir, ref_audio, ref_text), 
            daemon=True
        ).start()

    def run_generation_backend(self, input_file, output_dir, ref_audio, ref_text):
        """Your exact generation script logic, pulling parameters dynamically."""
        DELIMITER = "---"
        
        try:
            os.makedirs(output_dir, exist_ok=True)

            print("\n--- Starting OmniVoice Generation Process ---")
            print("Loading OmniVoice model into memory...")
            
            if torch.cuda.is_available():
                device = "cuda:0"
                dtype = torch.float16
                print("Using NVIDIA GPU (CUDA)")
            elif torch.backends.mps.is_available():
                device = "mps"
                dtype = torch.float16
                print("Using Apple Silicon (MPS)")
            else:
                device = "cpu"
                dtype = torch.float32
                print("Using CPU (Warning: This will be significantly slower)")

            model = OmniVoice.from_pretrained(
                "k2-fsa/OmniVoice", 
                device_map=device, 
                dtype=dtype
            )

            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            slides_text = [text.strip() for text in content.split(DELIMITER) if text.strip()]
            total_slides = len(slides_text)
            print(f"Found {total_slides} slides to process.\n")

            for index, text in enumerate(slides_text, start=1):
                filename = os.path.join(output_dir, f"audio{index}.wav")
                
                self.status_label.config(text=f"Processing slide {index} of {total_slides}...")
                
                print(f"[{index}/{total_slides}] Generating audio for Slide {index}...")
                print(f"Text snippet: \"{text[:50]}...\"")

                try:
                    audio = model.generate(
                        text=text,
                        ref_audio=ref_audio,
                        ref_text=ref_text,
                        preprocess_prompt=True
                    )

                    sf.write(filename, audio[0], 24000)
                    print(f"✓ Saved successfully -> {filename}\n")

                except Exception as slide_err:
                    print(f"✗ Error processing slide {index}: {slide_err}\n")

            print(f"All processing complete! Files saved to: {output_dir}")
            
            self.root.after(0, lambda: self.finish_success(output_dir))

        except Exception as e:
            print(f"Fatal script execution error: {e}")
            self.root.after(0, lambda: self.finish_failure(e))

    def finish_success(self, output_dir):
        self.translate_btn.config(state="normal")
        self.status_label.config(text="Generation complete!", foreground="green")
        messagebox.showinfo("Success!", f"All processing complete!\n\nYour audio files are waiting in:\n{output_dir}")

    def finish_failure(self, error_msg):
        self.translate_btn.config(state="normal")
        self.status_label.config(text="An error occurred.", foreground="red")
        messagebox.showerror("Execution Failed", f"The background script threw a critical error:\n\n{error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OmniVoiceTranslatorApp(root)
    root.mainloop()