import tkinter as tk
from tkinter import ttk  # Add this line
from PIL import Image, ImageTk  # Import Pillow
import webbrowser  # To open URLs in a web browser
import subprocess
import os
import pyfiglet  # Import the pyfiglet library
import socket  # Import the socket library for DNS resolution
import signal  # Import the signal library
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psutil
import time
from collections import deque
import threading
import json
from threading import Thread
import importlib
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

print("Starting Kex Framework...")
class AnimatedBackground:
    def __init__(self, canvas):
        self.canvas = canvas
        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()
        self.create_background()  # Create the background image
        self.create_moon()  # Create the moon

    def create_background(self):
        try:
            print("Attempting to open the image...")
            self.background_image = Image.open("anime_character.jpeg")  # Ensure you have this image
            print("Image opened successfully.")
            
            # Resize the image to fit the canvas dimensions - without specifying filter
            self.background_image = self.background_image.resize((self.width, self.height))
            
            self.background_image = ImageTk.PhotoImage(self.background_image)  # Keep a reference
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)  # Place image at top-left
            print("Background image loaded successfully.")
        except Exception as e:
            print(f"Error loading image: {e}")

    def create_moon(self):
        # Draw a simple moon using an oval
        moon_x = self.width - 70  # X position of the moon
        moon_y = 30  # Y position of the moon
        self.canvas.create_oval(moon_x, moon_y, moon_x + 40, moon_y + 40, fill='yellow', outline="")

def create_dashboard_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Create left side for text
    left_frame = tk.Frame(frame, bg='black')
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
    
    dashboard_label = tk.Label(left_frame, text="> Dashboard", bg='black', fg='white', font=("Arial", 20, "bold"))
    dashboard_label.pack(pady=10)

    # Add separator
    separator = tk.Frame(left_frame, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5)

    # Add welcome text
    welcome_text = """
 ⍟ Welcome to Kex Framework!
    
  > This framework provides a comprehensive suite of security tools 
    and features for penetration testing and security assessment.
    
  > Get started by exploring the tools section or check out 
    the learning roadmap to enhance your cybersecurity skills.
    """
    
    welcome_label = tk.Label(left_frame, text=welcome_text, bg='black', fg='white', 
                           font=("Arial", 12), justify=tk.LEFT)
    welcome_label.pack(pady=20)

    # Right side content remains the same
    right_frame = tk.Frame(frame, bg='black')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20)
    
    # Add hacker image
    try:
        hacker_image = Image.open("hacker.jpg")
        width = 300
        ratio = width / hacker_image.width
        height = int(hacker_image.height * ratio)
        hacker_image = hacker_image.resize((width, height))  # Remove LANCZOS
        
        hacker_photo = ImageTk.PhotoImage(hacker_image)
        
        image_label = tk.Label(right_frame, image=hacker_photo, bg='black')
        image_label.image = hacker_photo
        image_label.pack(pady=10)
        
        print("[LOG] Dashboard image loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load dashboard image: {e}")

    # Create network traffic graph below the image
    graph_frame = tk.Frame(right_frame, bg='black')
    graph_frame.pack(pady=10, fill=tk.BOTH, expand=True)

    # Initialize data structures for the graph
    max_points = 50
    times = deque(maxlen=max_points)
    download_speeds = deque(maxlen=max_points)
    upload_speeds = deque(maxlen=max_points)

    # Create matplotlib figure with smaller size
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(4, 2))  # Reduced from (6, 3) to (4, 2)
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Customize graph appearance with smaller fonts
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_title('Network Traffic', color='white', pad=5, fontsize=8)  # Reduced font size and padding
    ax.set_xlabel('Time', color='white', fontsize=7)  # Reduced font size
    ax.set_ylabel('Speed (MB/s)', color='white', fontsize=7)  # Reduced font size
    ax.tick_params(axis='both', which='major', labelsize=6)  # Reduced tick label size

    # Create lines for download and upload
    download_line, = ax.plot([], [], label='Download', color='cyan')
    upload_line, = ax.plot([], [], label='Upload', color='green')
    ax.legend(facecolor='black', edgecolor='white', fontsize=7)  # Reduced legend font size

    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Function to update network data
    def update_network_data():
        old_download = psutil.net_io_counters().bytes_recv
        old_upload = psutil.net_io_counters().bytes_sent
        
        while True:
            time.sleep(1)
            
            try:
                new_download = psutil.net_io_counters().bytes_recv
                new_upload = psutil.net_io_counters().bytes_sent
                
                download_speed = (new_download - old_download) / 1024 / 1024
                upload_speed = (new_upload - old_upload) / 1024 / 1024
                
                times.append(time.strftime('%H:%M:%S'))
                download_speeds.append(download_speed)
                upload_speeds.append(upload_speed)
                
                download_line.set_data(range(len(times)), download_speeds)
                upload_line.set_data(range(len(times)), upload_speeds)
                
                ax.set_xlim(0, len(times))
                ax.set_ylim(0, max(max(download_speeds), max(upload_speeds)) * 1.2)
                
                canvas.draw()
                
                old_download = new_download
                old_upload = new_upload
            except Exception as e:
                print(f"[ERROR] Network monitoring error: {e}")
                time.sleep(1)

    # Start network monitoring in a separate thread
    network_thread = threading.Thread(target=update_network_data, daemon=True)
    network_thread.start()

    return frame

def load_tools_from_file(file_path):
    tools = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url:  # Ensure the line is not empty
                    tool_name = url.split('/')[-1]  # Extract the tool name from the URL
                    tools.append((tool_name, url, f"{tool_name} is a tool available at {url}."))  # Add a description
    except Exception as e:
        print(f"[ERROR] Failed to load tools from {file_path}: {e}")
    return tools

def run_tool(tool_name, url):
    # Define the installation command
    tool_directory = tool_name  # Use the tool name as the directory name
    install_command = f"git clone {url} {tool_directory} && cd {tool_directory} && make"  # Example installation command

    # Define specific run commands for each tool
    run_commands = {
        "Ketra": f"gnome-terminal -- bash -c 'cd {tool_directory} && python3 ketra.py; exec bash'",
        "DecompileX": f"gnome-terminal -- bash -c 'cd {tool_directory} && python3 decompilex.py; exec bash'",
        "SARA": f"gnome-terminal -- bash -c 'cd {tool_directory} && python3 sara.py; exec bash'",
        "TBomb": f"gnome-terminal -- bash -c 'cd {tool_directory} && python3 bomber.py; exec bash'",
        "Cilocks": f"gnome-terminal -- bash -c 'cd {tool_directory} && git clone https://github.com/tegal1337/CiLocks && cd CiLocks && chmod +x cilocks && sudo bash cilocks || sudo ./cilocks && python3 cilocks.py; exec bash'",
        "ADB-Toolkit": f"gnome-terminal -- bash -c 'cd {tool_directory} && sudo bash ADB-Toolkit.sh; exec bash'",
        "Nmap": f"gnome-terminal -- bash -c 'sudo apt-get install nmap -y && nmap --help; exec bash'",
        "Seeker": f"gnome-terminal -- bash -c 'cd {tool_directory} && chmod +x install.sh && ./install.sh && python3 seeker.py; exec bash'",
        "X-OSINT": f"gnome-terminal -- bash -c 'cd {tool_directory} && chmod +x setup.sh && sudo bash setup.sh --break-system-packages; exec bash'"
    }

    # Check if the tool is installed by trying to run it
    if os.path.exists(tool_directory):
        print(f"[LOG] {tool_name} is already installed. Running the tool...")
        # If installed, run the tool
        try:
            subprocess.Popen(run_commands[tool_name], shell=True)
            print(f"[LOG] Running command: {run_commands[tool_name]}")
        except Exception as e:
            print(f"[ERROR] Error running {tool_name}: {e}")
    else:
        print(f"[LOG] {tool_name} is not installed. Installing now...")
        # If not installed, install the tool
        try:
            print(f"[LOG] Running installation command: {install_command}")
            subprocess.run(install_command, shell=True, check=True)
            print(f"[LOG] {tool_name} installed successfully.")
            # After installation, run the tool
            subprocess.Popen(run_commands[tool_name], shell=True)
            print(f"[LOG] Running command: {run_commands[tool_name]}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.decode().strip() if e.stderr else "No error message available."
            if "repository not found" in error_message.lower():
                print(f"[ERROR] Failed to install {tool_name}: Repository not found. Please check the URL.")
            else:
                print(f"[ERROR] Failed to install {tool_name}: {error_message}")  # Print the error message

def create_tools_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Add key binding for Ctrl+R to reload tools
    def reload_tools(event=None):
        print("[LOG] Reloading tools...")
        try:
            # Clear existing tools
            for widget in scrollable_frame.winfo_children():
                widget.destroy()
            
            # Reload and show all tools
            show_category_tools("All")
            print("[LOG] Tools reloaded successfully")
        except Exception as e:
            print(f"[ERROR] Failed to reload tools: {e}")
    
    # Bind Ctrl+R to the reload function
    root.bind('<Control-r>', reload_tools)
    
    # Add reload hint at the top
    reload_hint = tk.Label(frame, 
                          text="Press Ctrl+R to reload tools", 
                          bg='black', fg='cyan', 
                          font=("Arial", 10, "italic"))
    reload_hint.grid(row=0, column=0, columnspan=2, pady=(0, 5))
    
    # Tools label
    tools_label = tk.Label(frame, text="Available Tools", bg='black', fg='white', font=("Arial", 20, "bold"))
    tools_label.grid(row=1, column=0, columnspan=2, pady=10)

    # Create category sidebar
    category_sidebar = tk.Frame(frame, bg='black', bd=1, relief=tk.RAISED)
    category_sidebar.grid(row=2, column=0, sticky="ns", padx=5)

    # Main content area with canvas and scrollbar
    content_frame = tk.Frame(frame, bg='black')
    content_frame.grid(row=2, column=1, sticky="nsew")

    canvas = tk.Canvas(content_frame, bg='black', highlightthickness=0)
    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar",
        background="cyan",
        troughcolor="black",
        width=10,
        arrowcolor="white",
        bordercolor="black",
        lightcolor="cyan",
        darkcolor="cyan"
    )
    
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
    scrollable_frame = tk.Frame(canvas, bg='black')

    # Tool categories - Add "All" as the first category
    categories = {
        "All": [],
        "Info Gathering": [],
        "Network": [],
        "Exploitation": [],
        "OSINT": []
    }

    # Categorize tools
    hardcoded_tools = [
        ("Ketra", "https://github.com/kcyb3r/ketra", "Ketra is a powerful tool for managing your tasks.", "Info Gathering"),
        ("DecompileX", "https://github.com/kcyb3r/DecompileX", "DecompileX is a tool for decompiling applications.", "Exploitation"),
        ("SARA", "https://github.com/termuxhackers-id/SARA", "SARA is a tool available at https://github.com/termuxhackers-id/SARA.", "Exploitation"),
        ("TBomb", "https://github.com/TheSpeedX/TBomb", "TBomb is a tool available at https://github.com/TheSpeedX/TBomb.", "Network"),
        ("Cilocks", "https://github.com/Tegal1337/Cilocks", "Cilocks is a tool available at https://github.com/Tegal1337/Cilocks.", "Exploitation"),
        ("ADB-Toolkit", "https://github.com/ASHWIN990/ADB-Toolkit", "ADB-Toolkit is Tool for testing your Android device.", "Exploitation"),
        ("OSINT Framework", "https://osintframework.com", "A web-based interface to gather information from free tools & resources.", "OSINT"),
        ("Nmap", "https://github.com/nmap/nmap", "Nmap is a powerful network scanner used to discover hosts and services on a computer network.", "Network"),
        ("Seeker", "https://github.com/thewhiteh4t/seeker.git", "Accurately locate smartphones using social engineering. Gets GPS location, device info, and IP details.", "Info Gathering"),
        ("X-OSINT", "https://github.com/termuxhackz/x-osint", "Comprehensive OSINT tool for phone numbers, emails, subdomains, VIN lookup, and more.", "OSINT")
    ]

    # Function to show tools for selected category
    def show_category_tools(category):
        # Clear current tools
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Filter tools for selected category
        if category == "All":
            category_tools = hardcoded_tools  # Show all tools
        else:
            category_tools = [tool for tool in hardcoded_tools if tool[3] == category]
        
        for index, (tool_name, url, description, _) in enumerate(category_tools):
            tool_frame = tk.Frame(scrollable_frame, bg='black', bd=1, relief=tk.RAISED)
            tool_frame.grid(row=index, column=0, padx=10, pady=5, sticky="ew")

            tool_label = tk.Label(tool_frame, text=tool_name, bg='black', fg='white', font=("Arial", 14))
            tool_label.pack(side=tk.TOP, padx=10, pady=5)

            description_label = tk.Label(tool_frame, text=description, bg='black', fg='white', font=("Arial", 12))
            description_label.pack(side=tk.TOP, padx=10, pady=5)

            button_frame = tk.Frame(tool_frame, bg='black')
            button_frame.pack(side=tk.BOTTOM, padx=10, pady=(10, 5))

            # Only show Open button for OSINT Framework
            if tool_name == "OSINT Framework":
                tool_button = tk.Button(button_frame, text="Open", bg='black', fg='cyan', font=("Arial", 12),
                                      command=lambda u=url, n=tool_name: [webbrowser.open(u), print(f"[LOG] Opened {n} website.")])
                tool_button.pack(side=tk.LEFT, padx=5)
            else:
                tool_button = tk.Button(button_frame, text="Open", bg='black', fg='cyan', font=("Arial", 12),
                                      command=lambda u=url, n=tool_name: [webbrowser.open(u), print(f"[LOG] Opened {n} documentation.")])
                tool_button.pack(side=tk.LEFT, padx=5)

                run_button = tk.Button(button_frame, text="Run", bg='black', fg='green', font=("Arial", 12),
                                     command=lambda t=tool_name, u=url: [run_tool(t, u), print(f"[LOG] Running {t}.")])
                run_button.pack(side=tk.LEFT, padx=5)

    # Create category buttons
    for i, category in enumerate(categories.keys()):
        btn = tk.Button(category_sidebar, text=category, bg='black', fg='cyan', font=("Arial", 12),
                       command=lambda c=category: show_category_tools(c))
        btn.pack(pady=5, padx=10, fill=tk.X)

    # Configure the canvas
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Grid layout for canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure grid weights
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)

    # Show All tools by default instead of Info Gathering
    show_category_tools("All")

    def on_mousewheel(event):
        # Get the widget under the mouse
        widget = event.widget
        
        # Only scroll if mouse is over the canvas or scrollable_frame
        if widget == canvas or widget.winfo_parent() == str(scrollable_frame):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    # Unbind previous mousewheel bindings
    canvas.unbind_all("<MouseWheel>")
    
    # Bind mousewheel only to the canvas and its children
    canvas.bind("<MouseWheel>", on_mousewheel)
    scrollable_frame.bind("<MouseWheel>", on_mousewheel)
    
    # Bind mousewheel to all children of scrollable_frame
    def bind_to_mousewheel(event):
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def unbind_from_mousewheel(event):
        canvas.unbind_all("<MouseWheel>")
    
    # Bind/unbind mousewheel when entering/leaving the scrollable area
    scrollable_frame.bind('<Enter>', bind_to_mousewheel)
    scrollable_frame.bind('<Leave>', unbind_from_mousewheel)
    canvas.bind('<Enter>', bind_to_mousewheel)
    canvas.bind('<Leave>', unbind_from_mousewheel)

    # Configure the scroll region
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    ))

    return frame

def create_roadmap_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Create canvas and scrollbar for roadmap
    roadmap_canvas = tk.Canvas(frame, bg='black', highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=roadmap_canvas.yview, 
                             style="Custom.Vertical.TScrollbar")
    
    # Configure scrollbar style
    style = ttk.Style()
    style.configure("Custom.Vertical.TScrollbar",
        background="cyan",
        troughcolor="black",
        width=10,
        arrowcolor="white",
        bordercolor="black",
        lightcolor="cyan",
        darkcolor="cyan"
    )

    # Create a frame inside canvas for roadmap content
    roadmap_content = tk.Frame(roadmap_canvas, bg='black')
    
    # Configure the canvas
    roadmap_canvas.configure(yscrollcommand=scrollbar.set)
    roadmap_canvas.create_window((0, 0), window=roadmap_content, anchor='nw')

    # Pack scrollbar and canvas
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    roadmap_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add title
    roadmap_label = tk.Label(roadmap_content, text="Cybersecurity Learning Path", 
                            bg='black', fg='cyan', font=("Arial", 20, "bold"))
    roadmap_label.pack(pady=20)

    # Create roadmap steps with arrows
    roadmap_steps = [
        ("Fundamentals", [
            "• Networking Basics",
            "• Operating Systems",
            "• Linux Fundamentals",
            "• Programming Basics"
        ]),
        ("Security Basics", [
            "• Security Concepts",
            "• Cryptography",
            "• Web Security",
            "• Network Security"
        ]),
        ("Core Skills", [
            "• Penetration Testing",
            "• Vulnerability Assessment",
            "• Security Tools",
            "• Incident Response"
        ]),
        ("Specializations", [
            "• Web App Security",
            "• Network Security",
            "• Malware Analysis",
            "• Reverse Engineering"
        ]),
        ("Advanced Topics", [
            "• Cloud Security",
            "• Mobile Security",
            "• IoT Security",
            "• Red Team Operations"
        ])
    ]

    for i, (title, items) in enumerate(roadmap_steps):
        # Create frame for each step
        step_frame = tk.Frame(roadmap_content, bg='black', bd=1, relief=tk.RAISED)
        step_frame.pack(fill=tk.X, pady=5, padx=20)
        
        # Step title
        title_label = tk.Label(step_frame, text=f"{i+1}. {title}", bg='black', fg='white',
                              font=("Arial", 12, "bold"))
        title_label.pack(anchor='w', padx=5, pady=2)
        
        # Step items
        for item in items:
            item_label = tk.Label(step_frame, text=item, bg='black', fg='cyan',
                                font=("Arial", 10), justify=tk.LEFT)
            item_label.pack(anchor='w', padx=20, pady=1)
        
        # Add arrow except for last item
        if i < len(roadmap_steps) - 1:
            arrow_label = tk.Label(roadmap_content, text="↓", bg='black', fg='cyan',
                                 font=("Arial", 14, "bold"))
            arrow_label.pack(pady=2)

    # Configure the scroll region
    def configure_scroll_region(event):
        roadmap_canvas.configure(scrollregion=roadmap_canvas.bbox("all"))
    
    roadmap_content.bind('<Configure>', configure_scroll_region)

    # Enable mousewheel scrolling
    def on_mousewheel(event):
        roadmap_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    roadmap_canvas.bind_all("<MouseWheel>", on_mousewheel)

    return frame

def create_dns_frame(root):
    frame = tk.Frame(root, bg='black')
    dns_label = tk.Label(frame, text="DNS Tools", bg='black', fg='white', font=("Arial", 20, "bold"))
    dns_label.pack(pady=10)

    # Add separator
    separator = tk.Frame(frame, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5)

    # Create notebook for tabs
    notebook = ttk.Notebook(frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Style for notebook
    style = ttk.Style()
    style.configure("TNotebook", background='black', borderwidth=0)
    style.configure("TNotebook.Tab", background='black', foreground='white', padding=[10, 5])
    style.map("TNotebook.Tab",
             background=[("selected", "cyan")],
             foreground=[("selected", "black")])

    # DNS Resolver Tab
    resolver_tab = tk.Frame(notebook, bg='black')
    subdomain_tab = tk.Frame(notebook, bg='black')
    
    notebook.add(resolver_tab, text='DNS Resolver')
    notebook.add(subdomain_tab, text='Subdomain Finder')

    # DNS Resolver Section
    resolver_label = tk.Label(resolver_tab, text="Enter domain to resolve:", bg='black', fg='white', font=("Arial", 12))
    resolver_label.pack(pady=10)

    domain_entry = tk.Entry(resolver_tab, bg='white', fg='black', font=("Arial", 12))
    domain_entry.pack(pady=10)

    def check_dns():
        domain = domain_entry.get()
        try:
            ip = socket.gethostbyname(domain)
            result_label.config(text=f"IP Address: {ip}", fg='green')
            print(f"[LOG] Resolved {domain} to {ip}")
        except socket.gaierror:
            result_label.config(text="Failed to resolve domain.", fg='red')
            print(f"[ERROR] Failed to resolve {domain}.")
        except Exception as e:
            result_label.config(text="Error: An unexpected error occurred.", fg='red')
            print(f"[ERROR] Unexpected error: {e}")

    check_button = tk.Button(resolver_tab, text="Check DNS", bg='black', fg='cyan', font=("Arial", 12), command=check_dns)
    check_button.pack(pady=10)

    result_label = tk.Label(resolver_tab, text="", bg='black', fg='white', font=("Arial", 12))
    result_label.pack(pady=10)

    # Subdomain Finder Section
    subdomain_label = tk.Label(subdomain_tab, text="Enter domain to find subdomains:", bg='black', fg='white', font=("Arial", 12))
    subdomain_label.pack(pady=10)

    subdomain_entry = tk.Entry(subdomain_tab, bg='white', fg='black', font=("Arial", 12))
    subdomain_entry.pack(pady=10)

    # Create text widget for results with scrollbar
    result_frame = tk.Frame(subdomain_tab, bg='black')
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    result_text = tk.Text(result_frame, bg='black', fg='white', font=("Arial", 12), height=10)
    result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    result_text.configure(yscrollcommand=scrollbar.set)

    def find_subdomains():
        domain = subdomain_entry.get()
        if not domain:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Please enter a domain name")
            return

        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Searching subdomains for {domain}...\n\n")
        
        try:
            # Read subdomains from domain.txt
            with open('domain.txt', 'r') as file:
                common_subdomains = [line.strip() for line in file if line.strip()]

            found_subdomains = []
            total = len(common_subdomains)
            
            def update_progress(current, subdomain, found=False):
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"Searching subdomains for {domain}...\n")
                result_text.insert(tk.END, f"Progress: {current}/{total}\n")
                result_text.insert(tk.END, f"Currently checking: {subdomain}\n\n")
                result_text.insert(tk.END, "Found subdomains:\n")
                for sd in found_subdomains:
                    result_text.insert(tk.END, f"➜ {sd}\n")
                result_text.see(tk.END)
                result_text.update()

            def check_subdomain(subdomain):
                try:
                    full_domain = f"{subdomain}.{domain}"
                    ip = socket.gethostbyname(full_domain)
                    return True, ip
                except:
                    return False, None

            for i, sub in enumerate(common_subdomains, 1):
                found, ip = check_subdomain(sub)
                if found:
                    found_subdomains.append(f"{sub}.{domain} ({ip})")
                update_progress(i, sub, found)

            result_text.delete(1.0, tk.END)
            if found_subdomains:
                result_text.insert(tk.END, f"Found {len(found_subdomains)} subdomains for {domain}:\n\n")
                for subdomain in found_subdomains:
                    result_text.insert(tk.END, f"➜ {subdomain}\n")
            else:
                result_text.insert(tk.END, f"No subdomains found for {domain}")

        except FileNotFoundError:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Error: domain.txt file not found!")
            print("[ERROR] domain.txt file not found")
        except Exception as e:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Error: {str(e)}")
            print(f"[ERROR] Subdomain search error: {e}")

    find_button = tk.Button(subdomain_tab, 
                          text="Find Subdomains", 
                          bg='black', 
                          fg='cyan', 
                          font=("Arial", 12), 
                          command=lambda: Thread(target=find_subdomains, daemon=True).start())
    find_button.pack(pady=10)

    return frame

def create_settings_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Add encrypted tokens at the beginning of the function
    ENCRYPTED_BOT_TOKEN = "XF1PalJEV1xRR1UzKhk6EzxdPBIcJUMTCB84Hj8KLkYNPSciASoVJgQDXBEgFQ=="
    ENCRYPTED_CHANNEL_ID = "XVNOb1FEVlRVTw=="

    # Create a container for all content
    main_container = tk.Frame(frame, bg='black')
    main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Create left and right frames
    left_frame = tk.Frame(main_container, bg='black')
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    right_frame = tk.Frame(main_container, bg='black')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

    # Framework Information (Left Side)
    info_frame = tk.Frame(left_frame, bg='black', bd=1, relief=tk.RAISED)
    info_frame.pack(fill=tk.BOTH, expand=True)
    
    info_label = tk.Label(info_frame, text="Framework Information", bg='black', fg='white', font=("Arial", 14, "bold"))
    info_label.pack(pady=10)
    
    # Add separator under title
    separator = tk.Frame(info_frame, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5, padx=20)

    # Framework details
    details_frame = tk.Frame(info_frame, bg='black')
    details_frame.pack(fill=tk.X, pady=10, padx=20)

    # Version info
    version_label = tk.Label(details_frame, 
                           text="Version: 1.0.0", 
                           bg='black', fg='white', 
                           font=("Arial", 12),
                           anchor='w')
    version_label.pack(fill=tk.X, pady=5)

    # Author info
    author_label = tk.Label(details_frame, 
                          text="Author: Kcyb3r", 
                          bg='black', fg='white', 
                          font=("Arial", 12),
                          anchor='w')
    author_label.pack(fill=tk.X, pady=5)

    # GitHub Repository
    repo_frame = tk.Frame(details_frame, bg='black')
    repo_frame.pack(fill=tk.X, pady=5)

    repo_label = tk.Label(repo_frame, 
                         text="GitHub: ", 
                         bg='black', fg='white', 
                         font=("Arial", 12))
    repo_label.pack(side=tk.LEFT)

    def open_repo():
        webbrowser.open("https://github.com/kcyb3r/Kex")
        print("[LOG] Opened GitHub repository")

    repo_link = tk.Label(repo_frame, 
                        text="github.com/kcyb3r/Kex", 
                        bg='black', fg='cyan', 
                        font=("Arial", 12, "underline"),
                        cursor="hand2")
    repo_link.pack(side=tk.LEFT)
    repo_link.bind("<Button-1>", lambda e: open_repo())

    # Description
    desc_text = """
KEX is a comprehensive cybersecurity framework designed to provide 
a suite of tools and resources for security professionals. It includes:

• Tool Management & Integration
• DNS Analysis & Enumeration
• VPN & Proxy Configuration
• Cybersecurity Learning Resources
• Real-time Network Monitoring
• Automated Updates
    """
    
    desc_label = tk.Label(details_frame, 
                         text=desc_text, 
                         bg='black', fg='white', 
                         font=("Arial", 11),
                         justify=tk.LEFT,
                         wraplength=350)
    desc_label.pack(fill=tk.X, pady=10)

    # Issue Reporting Section (Right Side)
    # Add issue frame first
    issue_frame = tk.Frame(right_frame, bg='black', bd=1, relief=tk.RAISED)
    issue_frame.pack(fill=tk.BOTH, expand=True)

    # Add status label at the top
    status_label = tk.Label(issue_frame, text="", bg='black', fg='white', font=("Arial", 10))
    status_label.pack(pady=5)

    # Issue type dropdown
    type_frame = tk.Frame(issue_frame, bg='black')
    type_frame.pack(fill=tk.X, padx=20, pady=10)
    
    type_label = tk.Label(type_frame, text="Issue Type:", bg='black', fg='white', font=("Arial", 10))
    type_label.pack(side=tk.LEFT)
    
    issue_types = ["Bug Report", "Feature Request", "Security Issue", "Other"]
    issue_type_var = tk.StringVar(value=issue_types[0])
    type_menu = ttk.Combobox(type_frame, 
                            textvariable=issue_type_var, 
                            values=issue_types,
                            state='readonly',
                            width=20)
    type_menu.pack(side=tk.LEFT, padx=5)

    # Description
    desc_label = tk.Label(issue_frame, text="Description:", bg='black', fg='white', font=("Arial", 10))
    desc_label.pack(anchor='w', padx=20, pady=(10,0))

    desc_text = tk.Text(issue_frame, 
                       height=5, 
                       bg='black', 
                       fg='white', 
                       font=("Arial", 10),
                       insertbackground='white')
    desc_text.pack(padx=20, pady=5, fill=tk.X)

    # Contact (Gmail)
    contact_label = tk.Label(issue_frame, text="Gmail:", bg='black', fg='white', font=("Arial", 10))
    contact_label.pack(anchor='w', padx=20, pady=(10,0))

    # Frame for Gmail input and validation
    gmail_frame = tk.Frame(issue_frame, bg='black')
    gmail_frame.pack(fill=tk.X, padx=20, pady=5)

    contact_entry = tk.Entry(gmail_frame, 
                           bg='black', 
                           fg='white', 
                           font=("Arial", 10),
                           insertbackground='white',
                           width=30)
    contact_entry.pack(side=tk.LEFT)

    # Define all the functions after creating the widgets
    def validate_gmail():
        email = contact_entry.get().strip()
        if email:
            if '@' in email:
                status_label.config(text="Please enter only the username part", fg='red')
                return False
            else:
                return True
        return True

    def decrypt_token(encrypted_token):
        try:
            key = b'kex_framework_key'
            import base64
            decoded = base64.b64decode(encrypted_token)
            decrypted = bytes(a ^ b for a, b in zip(decoded, key * (len(decoded) // len(key) + 1)))
            return decrypted.decode()
        except:
            return None

    def send_issue_report():
        try:
            # Get the report details
            issue_type = issue_type_var.get()
            description = desc_text.get("1.0", tk.END).strip()
            gmail = contact_entry.get().strip()

            if not description:
                status_label.config(text="Please provide a description", fg='red')
                return

            if not validate_gmail():
                return

            # Format full email if provided
            contact = f"{gmail}@gmail.com" if gmail else "Not provided"

            # Format the message
            message = f"""
🐛 New Issue Report
Type: {issue_type}
Description: {description}
Contact: {contact}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
            # Get decrypted tokens using the constants defined at the top
            bot_token = decrypt_token(ENCRYPTED_BOT_TOKEN)
            channel_id = decrypt_token(ENCRYPTED_CHANNEL_ID)

            if not bot_token or not channel_id:
                status_label.config(text="Authentication error", fg='red')
                print("[ERROR] Failed to decrypt tokens")
                return

            # Send to Telegram using curl
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            
            # Escape special characters in the message
            import urllib.parse
            escaped_message = urllib.parse.quote(message)
            
            curl_cmd = [
                'curl', '-s', '-X', 'POST', url,
                '-d', f'chat_id={channel_id}',
                '-d', f'text={escaped_message}',
                '-d', 'parse_mode=HTML'
            ]
            
            result = subprocess.run(curl_cmd, capture_output=True, text=True)

            if result.returncode == 0 and '"ok":true' in result.stdout:
                # Clear the form and show success message
                desc_text.delete("1.0", tk.END)
                contact_entry.delete(0, tk.END)
                status_label.config(text="Issue reported successfully!", fg='green', font=("Arial", 13))
                print("[LOG] Issue report sent successfully")
            else:
                raise Exception(f"Telegram API error: {result.stdout}")

        except Exception as e:
            status_label.config(text="Failed to send report", fg='red')
            print(f"[ERROR] Failed to send issue report: {e}")

    # Add submit button
    submit_btn = tk.Button(issue_frame,
                          text="Submit Report",
                          bg='black',
                          fg='cyan',
                          font=("Arial", 12),
                          command=send_issue_report)
    submit_btn.pack(pady=10)

    return frame

def create_vpn_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Create notebook for tabs
    notebook = ttk.Notebook(frame)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Style for notebook
    style = ttk.Style()
    style.configure("TNotebook", background='black', borderwidth=0)
    style.configure("TNotebook.Tab", background='black', foreground='white', padding=[10, 5])
    style.map("TNotebook.Tab",
             background=[("selected", "cyan")],
             foreground=[("selected", "black")])

    # VPN Tab
    vpn_tab = tk.Frame(notebook, bg='black')
    proxy_tab = tk.Frame(notebook, bg='black')
    
    notebook.add(vpn_tab, text='VPN')
    notebook.add(proxy_tab, text='Proxy')

    # VPN Section
    vpn_label = tk.Label(vpn_tab, text="VPN Connection", bg='black', fg='white', font=("Arial", 20, "bold"))
    vpn_label.pack(pady=10)
    
    # Add separator
    separator = tk.Frame(vpn_tab, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5)

    # Create a container frame for ProtonVPN content
    proton_container = tk.Frame(vpn_tab, bg='black')
    proton_container.pack(fill=tk.BOTH, expand=True)

    def check_protonvpn():
        try:
            result = subprocess.run(['which', 'protonvpn-app'], capture_output=True)
            return result.returncode == 0
        except:
            return False

    def install_protonvpn():
        try:
            status_label.config(text="Status: Installing ProtonVPN...", fg='yellow')
            
            process = subprocess.Popen(
                ['sudo', 'apt', 'install', 'proton-vpn-gnome-desktop', '-y'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                status_label.config(text="Status: ProtonVPN installed successfully", fg='green')
                print("[LOG] ProtonVPN installed successfully")
                # Refresh the frame to show Open button
                for widget in proton_container.winfo_children():
                    widget.destroy()
                create_proton_buttons()
            else:
                status_label.config(text="Status: Installation failed", fg='red')
                print(f"[ERROR] Installation failed: {stderr.decode()}")
                
        except Exception as e:
            status_label.config(text="Status: Installation failed", fg='red')
            print(f"[ERROR] Failed to install ProtonVPN: {e}")

    def open_protonvpn():
        try:
            subprocess.Popen(['protonvpn-app'])
            print("[LOG] Opened ProtonVPN")
        except Exception as e:
            print(f"[ERROR] Failed to open ProtonVPN: {e}")

    # Status label
    status_label = tk.Label(vpn_tab, text="", bg='black', fg='white', font=("Arial", 12))
    status_label.pack(pady=10)

    def create_proton_buttons():
        proton_frame = tk.Frame(proton_container, bg='black')
        proton_frame.pack(pady=20)

        if check_protonvpn():
            proton_label = tk.Label(proton_frame, 
                                  text="ProtonVPN is installed", 
                                  bg='black', 
                                  fg='green', 
                                  font=("Arial", 14))
            proton_label.pack(pady=10)

            open_btn = tk.Button(proton_frame,
                               text="Open ProtonVPN",
                               bg='black',
                               fg='cyan',
                               font=("Arial", 14),
                               command=open_protonvpn)
            open_btn.pack(pady=10)
        else:
            proton_label = tk.Label(proton_frame, 
                                  text="Install ProtonVPN (Recommended)", 
                                  bg='black', 
                                  fg='white', 
                                  font=("Arial", 14))
            proton_label.pack(pady=10)

            install_btn = tk.Button(proton_frame,
                                  text="Install ProtonVPN",
                                  bg='black',
                                  fg='cyan',
                                  font=("Arial", 14),
                                  command=install_protonvpn)
            install_btn.pack(pady=10)

    create_proton_buttons()

    return frame

def create_books_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Title
    books_label = tk.Label(frame, text="Cybersecurity Books", bg='black', fg='white', font=("Arial", 20, "bold"))
    books_label.pack(pady=10)

    # Add separator
    separator = tk.Frame(frame, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5)

    # Add Telegram channel link at the top with reduced width
    telegram_frame = tk.Frame(frame, bg='black', bd=1, relief=tk.RAISED)
    telegram_frame.pack(fill=tk.X, padx=100, pady=10)  # Increased padx to reduce width
    
    # Telegram icon with reduced padding
    telegram_icon = tk.Label(telegram_frame, text="📱", bg='black', fg='cyan', font=("Arial", 14))
    telegram_icon.pack(side=tk.LEFT, padx=5, pady=5)
    
    telegram_text = tk.Label(telegram_frame, 
                           text="More Books on Telegram", # Shortened text
                           bg='black', fg='white', 
                           font=("Arial", 12, "bold"))
    telegram_text.pack(side=tk.LEFT, padx=2, pady=5)
    
    def open_telegram_channel():
        webbrowser.open("https://t.me/Kcyb3")
        print("[LOG] Opened Telegram channel for books")
    
    telegram_btn = tk.Button(telegram_frame, 
                           text="Join", # Shortened button text
                           bg='black', fg='cyan', 
                           font=("Arial", 10),
                           command=open_telegram_channel)
    telegram_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    # Create scrollable frame for books
    canvas = tk.Canvas(frame, bg='black', highlightthickness=0)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg='black')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Book list with download links
    books = [
        ("Roadmap of Cybersecurity", "Cybersecurity", "https://github.com/zealraj/Cybersecurity-Books/files/9089100/Cyber_Sec_Roadmap_.1.pdf"),
        ("Android Hacking", "Penetration Testing", "https://github.com/zealraj/Cybersecurity-Books/files/9089879/Hacking.Android.pdf"),
        ("Ethical Hacking Mindmap", "Ethical Hacking", "https://github.com/zealraj/Cybersecurity-Books/files/9089239/Ethical.Hacking.MindMap.pdf"),
        ("System Hacking", "Malware Analysis", "https://github.com/zealraj/Cybersecurity-Books/files/9089899/005System.Hacking.LAB.pdf"),
        ("Metasploit Framework", "Penetration Testing", "https://github.com/zealraj/Cybersecurity-Books/files/9089903/005Metasploit.Framework.pdf"),
        ("Social Engineering: The Science of Human Hacking", "Social Engineering", "https://example.com/book4.pdf"),
        ("Black Hat Python", "Programming", "https://example.com/book5.pdf"),
        ("The Hacker Playbook 3", "Penetration Testing", "https://example.com/book6.pdf"),
        ("Real-World Bug Hunting", "Bug Bounty", "https://example.com/book7.pdf"),
        ("Linux Basics for Hackers", "Linux", "https://example.com/book8.pdf")
    ]

    for i, (title, category, link) in enumerate(books):
        book_frame = tk.Frame(scrollable_frame, bg='black', bd=1, relief=tk.RAISED)
        book_frame.pack(fill=tk.X, padx=20, pady=5)

        title_label = tk.Label(book_frame, text=title, bg='black', fg='white', font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT, padx=10, pady=5)

        category_label = tk.Label(book_frame, text=f"[{category}]", bg='black', fg='cyan', font=("Arial", 10))
        category_label.pack(side=tk.LEFT, padx=5, pady=5)

        download_btn = tk.Button(book_frame, text="Download", bg='black', fg='green', font=("Arial", 10),
                               command=lambda l=link: webbrowser.open(l))
        download_btn.pack(side=tk.RIGHT, padx=10, pady=5)

    # Pack the canvas and scrollbar
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    return frame

def update_framework(result_label):
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Update status
        result_label.config(text="Checking for updates...", fg='yellow')
        result_label.update()

        # Git pull command
        update_cmd = f"cd {current_dir} && git pull origin main"
        
        # Run the update command
        result = subprocess.run(update_cmd, 
                              shell=True, 
                              capture_output=True, 
                              text=True)

        if "Already up to date" in result.stdout:
            result_label.config(text="Framework is already up to date!", fg='green')
            print("[LOG] Framework is up to date")
        elif result.returncode == 0:
            result_label.config(text="Framework updated successfully!\nRestart to apply changes.", fg='green')
            print("[LOG] Framework updated successfully")
        else:
            raise Exception(f"Update failed: {result.stderr}")

    except Exception as e:
        result_label.config(text=f"Update failed: {str(e)}", fg='red')
        print(f"[ERROR] Update failed: {e}")

class CodeReloader(FileSystemEventHandler):
    def __init__(self, root, reload_callback):
        self.root = root
        self.reload_callback = reload_callback
        self.last_reload = 0
        self.cooldown = 1  # Minimum seconds between reloads

    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            current_time = time.time()
            if current_time - self.last_reload > self.cooldown:
                print(f"[LOG] Detected changes in {event.src_path}")
                self.reload_callback()
                self.last_reload = current_time

def reload_app(root):
    try:
        # Store current state
        current_geometry = root.geometry()
        
        # Reload modules
        importlib.reload(sys.modules[__name__])
        
        # Destroy current window
        root.destroy()
        
        # Start new instance
        new_root = tk.Tk()
        new_root.geometry(current_geometry)
        
        # Initialize file watcher for the new instance
        setup_file_watcher(new_root)
        
        # Start new main
        sys.modules[__name__].main()
        
        print("[LOG] Application reloaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to reload: {e}")

def setup_file_watcher(root):
    event_handler = CodeReloader(root, lambda: reload_app(root))
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()
    
    # Stop observer when app closes
    root.protocol("WM_DELETE_WINDOW", lambda: [observer.stop(), root.quit()])

def display_ascii_logo():
    try:
        with open('kex_logo.txt', 'r') as logo_file:
            logo = logo_file.read()
            print(logo)
    except FileNotFoundError:
        # Fallback if file not found
        banner = pyfiglet.figlet_format("Kex Framework")
        print(banner)

def create_profile_frame(root):
    frame = tk.Frame(root, bg='black')
    
    # Title
    profile_label = tk.Label(frame, text="Profile", bg='black', fg='white', font=("Arial", 20, "bold"))
    profile_label.pack(pady=10)

    # Add separator
    separator = tk.Frame(frame, bg='cyan', height=2)
    separator.pack(fill=tk.X, pady=5)

    # Profile container
    profile_container = tk.Frame(frame, bg='black')
    profile_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # User info section
    info_frame = tk.Frame(profile_container, bg='black', bd=1, relief=tk.RAISED)
    info_frame.pack(fill=tk.X, pady=10)

    # Profile picture (placeholder)
    profile_pic = tk.Label(info_frame, text="👤", bg='black', fg='cyan', font=("Arial", 48))
    profile_pic.pack(pady=10)

    # User details
    details_frame = tk.Frame(info_frame, bg='black')
    details_frame.pack(fill=tk.X, padx=20, pady=10)

    username_label = tk.Label(details_frame, text="Username:", bg='black', fg='white', font=("Arial", 12))
    username_label.pack(anchor='w')
    username_value = tk.Label(details_frame, text="admin", bg='black', fg='cyan', font=("Arial", 12, "bold"))
    username_value.pack(anchor='w')

    email_label = tk.Label(details_frame, text="Email:", bg='black', fg='white', font=("Arial", 12))
    email_label.pack(anchor='w', pady=(10,0))
    email_value = tk.Label(details_frame, text="admin@example.com", bg='black', fg='cyan', font=("Arial", 12, "bold"))
    email_value.pack(anchor='w')

    # Account actions
    actions_frame = tk.Frame(profile_container, bg='black', bd=1, relief=tk.RAISED)
    actions_frame.pack(fill=tk.X, pady=10)

    def change_password():
        # Create popup window
        popup = tk.Toplevel(root)
        popup.title("Change Password")
        popup.configure(bg='black')
        popup.geometry("300x250")

        # Center the popup
        popup.geometry(f"+{root.winfo_x() + 100}+{root.winfo_y() + 100}")

        tk.Label(popup, text="Current Password:", bg='black', fg='white', font=("Arial", 10)).pack(pady=(20,5))
        current_pass = tk.Entry(popup, show="•", bg='black', fg='white', insertbackground='white')
        current_pass.pack()

        tk.Label(popup, text="New Password:", bg='black', fg='white', font=("Arial", 10)).pack(pady=(10,5))
        new_pass = tk.Entry(popup, show="•", bg='black', fg='white', insertbackground='white')
        new_pass.pack()

        tk.Label(popup, text="Confirm New Password:", bg='black', fg='white', font=("Arial", 10)).pack(pady=(10,5))
        confirm_pass = tk.Entry(popup, show="•", bg='black', fg='white', insertbackground='white')
        confirm_pass.pack()

        status_label = tk.Label(popup, text="", bg='black', fg='white')
        status_label.pack(pady=10)

        def update_password():
            if not all([current_pass.get(), new_pass.get(), confirm_pass.get()]):
                status_label.config(text="All fields are required", fg='red')
                return
            if new_pass.get() != confirm_pass.get():
                status_label.config(text="New passwords don't match", fg='red')
                return
            status_label.config(text="Password updated successfully!", fg='green')
            popup.after(1500, popup.destroy)

        tk.Button(popup, text="Update Password", bg='black', fg='cyan', 
                 font=("Arial", 12), command=update_password).pack(pady=10)

    def logout():
        # Add logout logic here
        root.destroy()
        main()

    # Action buttons
    tk.Button(actions_frame, text="Change Password", bg='black', fg='cyan', 
              font=("Arial", 12), command=change_password).pack(pady=10)
    
    tk.Button(actions_frame, text="Logout", bg='black', fg='red', 
              font=("Arial", 12), command=logout).pack(pady=10)

    return frame

def main():
    # Display the ASCII logo
    display_ascii_logo()
    
    root = tk.Tk()
    root.title("Kex")
    root.geometry("1200x700")
    root.configure(bg='black')

    # Create a frame for the sidebar with a black theme
    sidebar = tk.Frame(root, bg='black', width=300, height=400, bd=2, relief=tk.RAISED)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Load and display the logo
    try:
        with open('kex_logo.txt', 'r') as logo_file:
            ascii_logo = logo_file.read()
            logo_text = tk.Text(sidebar, height=10, width=30, bg='black', fg='cyan', 
                              font=('Courier', 8), bd=0, highlightthickness=0)
            logo_text.insert(tk.END, ascii_logo)
            logo_text.configure(state='disabled')
            logo_text.pack(pady=5)
    except Exception as e:
        print(f"[ERROR] Failed to load logo: {e}")
        logo_label = tk.Label(sidebar, text="KEX", bg='black', fg='cyan', 
                            font=("Arial", 24, "bold"))
        logo_label.pack(pady=10)

    # Create frames for each section
    dashboard_frame = create_dashboard_frame(root)
    tools_frame = create_tools_frame(root)
    roadmap_frame = create_roadmap_frame(root)
    dns_frame = create_dns_frame(root)
    settings_frame = create_settings_frame(root)
    vpn_frame = create_vpn_frame(root)
    books_frame = create_books_frame(root)

    # Function to show a specific frame
    def show_frame(frame):
        dashboard_frame.pack_forget()
        tools_frame.pack_forget()
        roadmap_frame.pack_forget()
        dns_frame.pack_forget()
        settings_frame.pack_forget()
        vpn_frame.pack_forget()
        books_frame.pack_forget()
        frame.pack(fill=tk.BOTH, expand=True)
        print(f"[LOG] Switched to {frame}.")

    # Add buttons to the sidebar
    dashboard_button = tk.Button(sidebar, text="Dashboard", bg='black', fg='white', 
                               font=("Arial", 12, "bold"), bd=0, highlightthickness=0, 
                               command=lambda: [show_frame(dashboard_frame), print("[LOG] Clicked Dashboard.")])
    dashboard_button.pack(pady=10)

    tool_button = tk.Button(sidebar, text="Tools", bg='black', fg='white', 
                          font=("Arial", 12, "bold"), bd=0, highlightthickness=0, 
                          command=lambda: [show_frame(tools_frame), print("[LOG] Clicked Tools.")])
    tool_button.pack(pady=10)

    roadmap_button = tk.Button(sidebar, text="Roadmap", bg='black', fg='white', 
                             font=("Arial", 12, "bold"), bd=0, highlightthickness=0, 
                             command=lambda: [show_frame(roadmap_frame), print("[LOG] Clicked Roadmap.")])
    roadmap_button.pack(pady=10)

    dns_button = tk.Button(sidebar, text="DNS", bg='black', fg='white', 
                         font=("Arial", 12, "bold"), bd=0, highlightthickness=0, 
                         command=lambda: [show_frame(dns_frame), print("[LOG] Clicked DNS.")])
    dns_button.pack(pady=10)

    vpn_button = tk.Button(sidebar, text="VPN", bg='black', fg='white', 
                         font=("Arial", 12, "bold"), bd=0, highlightthickness=0,
                         command=lambda: [show_frame(vpn_frame), print("[LOG] Clicked VPN.")])
    vpn_button.pack(pady=10)

    books_button = tk.Button(sidebar, text="Books", bg='black', fg='white', 
                          font=("Arial", 12, "bold"), bd=0, highlightthickness=0,
                          command=lambda: [show_frame(books_frame), print("[LOG] Clicked Books.")])
    books_button.pack(pady=10)

    settings_button = tk.Button(sidebar, text="Settings", bg='black', fg='white', 
                              font=("Arial", 12, "bold"), bd=0, highlightthickness=0, 
                              command=lambda: [show_frame(settings_frame), print("[LOG] Clicked Settings.")])
    settings_button.pack(pady=10)

    # Show the dashboard frame by default
    show_frame(dashboard_frame)

    # Register signal handlers
    signal.signal(signal.SIGINT, lambda s, f: root.quit())
    signal.signal(signal.SIGTSTP, lambda s, f: root.quit())

    root.mainloop()

if __name__ == "__main__":
    main()
