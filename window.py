import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from typing import Optional
from ml.model import SkinFeatureAnalyzer

class SkinAnalyzerWindow:
    """
    Handles the graphical user interface for webcam capture and analysis display.
    """

    def __init__(self, root: tk.Tk, window_title: str) -> None:
        """
        Initializes the main window, UI elements, and video stream.

        Args:
            root: The main Tkinter root instance.
            window_title: Title of the window.
        """
        self.root = root
        self.root.title(window_title)

        # Initialize ML model
        try:
            self.analyzer = SkinFeatureAnalyzer()
        except Exception as e:
            messagebox.showerror("Model Error", f"Could not load ML model: {e}")
            self.root.destroy()
            return

        # Initialize Webcam, default index 0
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            messagebox.showerror("Camera Error", "Could not access webcam.")
            self.root.destroy()
            return

        self.canvas_width = 640
        self.canvas_height = 480

        # UI Layout
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(padx=10, pady=10)

        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(fill=tk.X, padx=10, pady=5)

        self.btn_capture = tk.Button(self.btn_frame, text="Capture and Analyze", command=self.capture_and_analyze)
        self.btn_capture.pack(pady=5)

        self.lbl_info = tk.Label(root, text="IMPORTANT: This is not medical advice.", fg="red", font=("Helvetica", 10, "bold"))
        self.lbl_info.pack(pady=5)

        self.result_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
        self.result_text.pack(padx=10, pady=10)

        # Start video loop
        self.current_frame: Optional[Image.Image] = None
        self.update_webcam()

    def update_webcam(self) -> None:
        """Reads frame from webcam, updates canvas, and schedules next update."""
        ret, frame = self.vid.read()
        if ret:
            # Convert OpenCV BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_frame = Image.fromarray(frame_rgb)
            self.photo = ImageTk.PhotoImage(image=self.current_frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        
        # Schedule next update in 15ms
        self.root.after(15, self.update_webcam)

    def capture_and_analyze(self) -> None:
        """Captures current frame, passes it to the model, and displays results."""
        if self.current_frame is None:
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "Analyzing...\n")
        self.result_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

        # Perform analysis
        results = self.analyzer.analyze_image(self.current_frame)

        # Display results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete('1.0', tk.END)
        
        display_text = "Analysis Results (Informational Only):\n\n"
        if not results:
            display_text += "No valid results or error occurred."
        else:
            for res in results:
                label = res.get('label', 'Unknown')
                score = float(res.get('score', 0.0))
                display_text += f"Feature: {label}, Confidence: {score:.2f}\n"

        display_text += ("\nDisclaimer: This analysis is for informational purposes only.\n"
                        "It is NOT a medical diagnosis. Consult a dermatologist\n"
                        "or healthcare professional for medical advice.")
                        
        self.result_text.insert(tk.END, display_text)
        self.result_text.config(state=tk.DISABLED)

    def __del__(self) -> None:
        """Ensures resources are released when window is closed."""
        if hasattr(self, 'vid') and self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    # Test stub for ui/window.py development/testing
    import sys
    import os
    # Add root directory to sys.path to resolve ml.model import when running directly
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    main_root = tk.Tk()
    app = SkinAnalyzerWindow(main_root, "Skin Feature Analyzer (DEV)")
    main_root.mainloop()