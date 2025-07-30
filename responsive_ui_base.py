import tkinter as tk
from tkinter import ttk

class ResponsiveUI:
    """Base class for responsive UI components"""
    
    def __init__(self):
        self.screen_width = 0
        self.screen_height = 0
        self.scale_factor = 1.0
        
    def setup_responsive_window(self, root, title, min_width=800, min_height=600):
        """Setup responsive window with proper scaling"""
        root.title(title)
        
        # Get screen dimensions
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        
        # Calculate scale factor based on screen size
        if self.screen_width >= 1920:  # 1080p or higher
            self.scale_factor = 1.2
            window_width = int(min_width * 1.3)
            window_height = int(min_height * 1.2)
        elif self.screen_width >= 1366:  # 720p
            self.scale_factor = 1.0
            window_width = min_width
            window_height = min_height
        else:  # Smaller screens
            self.scale_factor = 0.8
            window_width = int(min_width * 0.9)
            window_height = int(min_height * 0.9)
        
        # Set window size and position
        x = (self.screen_width - window_width) // 2
        y = (self.screen_height - window_height) // 2
        
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.minsize(int(min_width * 0.8), int(min_height * 0.8))
        
        # Configure root for responsiveness
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        
        return window_width, window_height
    
    def get_font_size(self, base_size):
        """Get scaled font size"""
        return int(base_size * self.scale_factor)
    
    def get_button_size(self, base_width, base_height):
        """Get scaled button size"""
        return int(base_width * self.scale_factor), int(base_height * self.scale_factor)
    
    def get_padding(self, base_padding):
        """Get scaled padding"""
        return int(base_padding * self.scale_factor)
    
    def create_responsive_frame(self, parent, **kwargs):
        """Create responsive frame with proper grid configuration"""
        frame = tk.Frame(parent, **kwargs)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        return frame
    
    def create_scrollable_frame(self, parent, **kwargs):
        """Create scrollable frame for long content"""
        # Main container
        container = tk.Frame(parent, **kwargs)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure container grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Mouse wheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        return container, scrollable_frame
    
    def create_responsive_button(self, parent, text, command=None, style="primary", **kwargs):
        """Create responsive button with proper scaling"""
        # Button styles
        styles = {
            "primary": {"bg": "#007bff", "fg": "white", "activebackground": "#0056b3"},
            "success": {"bg": "#28a745", "fg": "white", "activebackground": "#1e7e34"},
            "danger": {"bg": "#dc3545", "fg": "white", "activebackground": "#c82333"},
            "warning": {"bg": "#ffc107", "fg": "black", "activebackground": "#e0a800"},
            "info": {"bg": "#17a2b8", "fg": "white", "activebackground": "#138496"},
            "secondary": {"bg": "#6c757d", "fg": "white", "activebackground": "#545b62"},
            "dark": {"bg": "#343a40", "fg": "white", "activebackground": "#23272b"}
        }
        
        # Get style colors
        colors = styles.get(style, styles["primary"])
        
        # Default button properties
        button_props = {
            "font": ("Arial", self.get_font_size(12), "bold"),
            "relief": "raised",
            "borderwidth": 2,
            "cursor": "hand2",
            **colors,
            **kwargs
        }
        
        button = tk.Button(parent, text=text, command=command, **button_props)
        return button
    
    def create_responsive_label(self, parent, text, style="normal", **kwargs):
        """Create responsive label with proper scaling"""
        # Label styles
        styles = {
            "title": {"font": ("Arial", self.get_font_size(24), "bold")},
            "subtitle": {"font": ("Arial", self.get_font_size(18), "bold")},
            "heading": {"font": ("Arial", self.get_font_size(16), "bold")},
            "normal": {"font": ("Arial", self.get_font_size(12))},
            "small": {"font": ("Arial", self.get_font_size(10))}
        }
        
        # Get style properties
        style_props = styles.get(style, styles["normal"])
        
        label_props = {
            **style_props,
            **kwargs
        }
        
        label = tk.Label(parent, text=text, **label_props)
        return label
    
    def create_responsive_entry(self, parent, **kwargs):
        """Create responsive entry with proper scaling"""
        entry_props = {
            "font": ("Arial", self.get_font_size(12)),
            "relief": "sunken",
            "borderwidth": 2,
            **kwargs
        }
        
        entry = tk.Entry(parent, **entry_props)
        return entry
    
    def create_responsive_text(self, parent, **kwargs):
        """Create responsive text widget with proper scaling"""
        text_props = {
            "font": ("Arial", self.get_font_size(11)),
            "relief": "sunken",
            "borderwidth": 2,
            "wrap": "word",
            **kwargs
        }
        
        text_widget = tk.Text(parent, **text_props)
        return text_widget
    
    def create_responsive_labelframe(self, parent, text, **kwargs):
        """Create responsive labelframe with proper scaling"""
        frame_props = {
            "font": ("Arial", self.get_font_size(14), "bold"),
            "relief": "groove",
            "borderwidth": 2,
            **kwargs
        }
        
        labelframe = tk.LabelFrame(parent, text=text, **frame_props)
        return labelframe