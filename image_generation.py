import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw
import os
import csv
import glob

class CharacterGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Handwritten Character Generator (Anti-Aliased)")
        
        # Configuration
        self.canvas_size = 480
        self.target_size = 48
        self.pen_width = 28  # Thicker pen in the high-res canvas (will be ~2.8 pixels thick when downscaled)
        
        # Data directory setup
        self.dataset_dir = "dataset"
        os.makedirs(self.dataset_dir, exist_ok=True)
        
        # Initialize variables
        self.classes = [str(i) for i in range(10)] + [chr(i) for i in range(ord('A'), ord('Z')+1)]
        self.writers = [f"W{i:02d}" for i in range(1, 7)]
        
        self.current_class = tk.StringVar(value=self.classes[0])
        self.current_writer = tk.StringVar(value=self.writers[0])
        self.sample_id = tk.StringVar(value="001")
        
        self.is_drawing = False
        self.last_x = None
        self.last_y = None
        
        self.setup_ui()
        self.init_canvas()
        self.update_sample_id()

    def get_metadata_file(self):
        # Using a writer-specific CSV to avoid Git merge conflicts for your group!
        return os.path.join(self.dataset_dir, f"metadata_{self.current_writer.get()}.csv")

    def setup_ui(self):
        # Top Frame for controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Writer Dropdown
        ttk.Label(control_frame, text="Writer ID:").pack(side=tk.LEFT, padx=5)
        writer_cb = ttk.Combobox(control_frame, textvariable=self.current_writer, values=self.writers, state="readonly", width=5)
        writer_cb.pack(side=tk.LEFT, padx=5)
        writer_cb.bind("<<ComboboxSelected>>", lambda e: self.update_sample_id())
        
        # Class Dropdown
        ttk.Label(control_frame, text="Target Class:").pack(side=tk.LEFT, padx=5)
        class_cb = ttk.Combobox(control_frame, textvariable=self.current_class, values=self.classes, state="readonly", width=5)
        class_cb.pack(side=tk.LEFT, padx=5)
        class_cb.bind("<<ComboboxSelected>>", lambda e: self.update_sample_id())
        
        # Sample ID Display
        ttk.Label(control_frame, text="Next Sample:").pack(side=tk.LEFT, padx=5)
        ttk.Label(control_frame, textvariable=self.sample_id, font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Canvas Frame
        canvas_frame = ttk.Frame(self.root, padding="10")
        canvas_frame.pack()
        
        self.canvas = tk.Canvas(canvas_frame, width=self.canvas_size, height=self.canvas_size, bg="white", highlightbackground="black", highlightthickness=1)
        self.canvas.pack()
        
        # Bindings for drawing
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Buttons Frame
        btn_frame = ttk.Frame(self.root, padding="10")
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        ttk.Button(btn_frame, text="Save & Next", command=self.save_image).pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        # Status Bar
        self.status_var = tk.StringVar(value="Ready. Draw using smooth, thick strokes.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding="2")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def init_canvas(self):
        # We draw on a high-resolution 480x480 canvas for smooth curves
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), 255)
        self.draw_img = ImageDraw.Draw(self.image)
        self.canvas.delete("all")
        self.last_x = None
        self.last_y = None

    def start_draw(self, event):
        self.is_drawing = True
        self.last_x, self.last_y = event.x, event.y
        # Draw a single dot if they just click
        r = self.pen_width / 2
        self.canvas.create_oval(event.x - r, event.y - r, event.x + r, event.y + r, fill="black", outline="black")
        self.draw_img.ellipse([event.x - r, event.y - r, event.x + r, event.y + r], fill=0)

    def stop_draw(self, event):
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def draw(self, event):
        if not self.is_drawing or self.last_x is None:
            return
            
        x, y = event.x, event.y
        
        # Draw smooth line on UI canvas
        self.canvas.create_line(self.last_x, self.last_y, x, y, 
                                width=self.pen_width, fill="black", 
                                capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True)
                                
        # Draw on PIL Image backend
        self.draw_img.line([(self.last_x, self.last_y), (x, y)], fill=0, width=self.pen_width, joint="curve")
        
        self.last_x, self.last_y = x, y

    def clear_canvas(self):
        self.init_canvas()
        self.status_var.set("Canvas cleared.")

    def update_sample_id(self):
        cls = self.current_class.get()
        writer = self.current_writer.get()
        
        class_dir = os.path.join(self.dataset_dir, cls)
        
        if not os.path.exists(class_dir):
            self.sample_id.set("001")
            return
            
        pattern = os.path.join(class_dir, f"{cls}_{writer}_*.png")
        files = glob.glob(pattern)
        
        max_id = 0
        for f in files:
            basename = os.path.basename(f)
            try:
                parts = basename.split('_')
                if len(parts) >= 3:
                    sample_str = parts[2].split('.')[0]
                    sample_num = int(sample_str)
                    if sample_num > max_id:
                        max_id = sample_num
            except Exception:
                pass
                
        self.sample_id.set(f"{max_id + 1:03d}")

    def save_image(self):
        cls = self.current_class.get()
        writer = self.current_writer.get()
        sample = self.sample_id.get()
        
        class_dir = os.path.join(self.dataset_dir, cls)
        os.makedirs(class_dir, exist_ok=True)
        
        filename = f"{cls}_{writer}_{sample}.png"
        filepath = os.path.join(class_dir, filename)
        
        # IMPORTANT: Downscale the high-res 480x480 drawing to 48x48 
        # using Lanczos resampling. This mathematically guarantees high-quality,
        # anti-aliased grayscale strokes (preserving intensity variation!)
        final_image = self.image.resize((self.target_size, self.target_size), Image.Resampling.LANCZOS)
        final_image.save(filepath)
        
        # Save metadata to writer-specific CSV to avoid Git conflicts
        metadata_csv = self.get_metadata_file()
        file_exists = os.path.exists(metadata_csv)
        with open(metadata_csv, 'a', newline='') as csvfile:
            writer_csv = csv.writer(csvfile)
            if not file_exists:
                writer_csv.writerow(['filename', 'label', 'writer_id', 'sample_id'])
            writer_csv.writerow([filename, cls, writer, sample])
            
        self.status_var.set(f"Saved {filename} (Anti-Aliased)")
        self.clear_canvas()
        self.update_sample_id()

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterGeneratorApp(root)
    root.resizable(False, False)
    root.mainloop()
