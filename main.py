import tkinter as tk
from tkinter import ttk  # Add this line
from PIL import Image, ImageTk  # Import Pillow
import webbrowser  # To open URLs in a web browser
import subprocess
import os
import pyfiglet  # Import the pyfiglet library
import socket  # Import the socket library for DNS resolution
import signal  # Import the signal library

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
            
            # Resize the image to fit the canvas dimensions
            self.background_image = self.background_image.resize((self.width, self.height), Image.LANCZOS)  # Use LANCZOS for resizing
            
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
    dashboard_label = tk.Label(frame, text="Welcome to the Dashboard", bg='black', fg='white', font=("Arial", 20, "bold"))
    dashboard_label.pack(pady=10)

    info_label = tk.Label(frame, text="Here you can manage your tools and settings.", bg='black', fg='white', font=("Arial", 14))
    info_label.pack(pady=10)

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
    tools_label = tk.Label(frame, text="Available Tools", bg='black', fg='white', font=("Arial", 20, "bold"))
    tools_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Create category sidebar
    category_sidebar = tk.Frame(frame, bg='black', bd=1, relief=tk.RAISED)
    category_sidebar.grid(row=1, column=0, sticky="ns", padx=5)

    # Main content area with canvas and scrollbar
    content_frame = tk.Frame(frame, bg='black')
    content_frame.grid(row=1, column=1, sticky="nsew")

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
        ("SARA", "https://github.com/termuxhackers-id/SARA", "SARA is a tool available at https://github.com/termuxhackers-id/SARA.", "OSINT"),
        ("TBomb", "https://github.com/TheSpeedX/TBomb", "TBomb is a tool available at https://github.com/TheSpeedX/TBomb.", "Network"),
        ("Cilocks", "https://github.com/Tegal1337/Cilocks", "Cilocks is a tool available at https://github.com/Tegal1337/Cilocks.", "Exploitation"),
        ("ADB-Toolkit", "https://github.com/ASHWIN990/ADB-Toolkit", "ADB-Toolkit is Tool for testing your Android device.", "Exploitation")
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
    frame.grid_rowconfigure(1, weight=1)

    # Show All tools by default instead of Info Gathering
    show_category_tools("All")

    return frame

def create_about_frame(root):
    frame = tk.Frame(root, bg='black')
    about_label = tk.Label(frame, text="About Kex", bg='black', fg='white', font=("Arial", 20, "bold"))
    about_label.pack(pady=10)

    info_label = tk.Label(frame, text="Kex is a powerful tool for managing your tasks.", bg='black', fg='white', font=("Arial", 14))
    info_label.pack(pady=10)

    additional_info = tk.Label(frame, text="Developed by Kcyb3r.", bg='black', fg='white', font=("Arial", 12))
    additional_info.pack(pady=10)

    return frame

def create_dns_frame(root):
    frame = tk.Frame(root, bg='black')
    dns_label = tk.Label(frame, text="DNS Management", bg='black', fg='white', font=("Arial", 20, "bold"))
    dns_label.pack(pady=10)

    info_label = tk.Label(frame, text="Enter a domain name to check its DNS.", bg='black', fg='white', font=("Arial", 14))
    info_label.pack(pady=10)

    # Entry field for domain name
    domain_entry = tk.Entry(frame, bg='white', fg='black', font=("Arial", 12))
    domain_entry.pack(pady=10)

    # Function to check DNS
    def check_dns():
        domain = domain_entry.get().strip()  # Get the domain and strip whitespace
        if not domain:
            result_label.config(text="Error: Please enter a domain name.", fg='red')
            print("[ERROR] No domain entered.")
            return

        try:
            ip_address = socket.gethostbyname(domain)
            result_label.config(text=f"IP Address: {ip_address}", fg='green')
            print(f"[LOG] Resolved {domain} to {ip_address}.")
        except socket.gaierror:
            result_label.config(text="Error: Domain not found.", fg='red')
            print(f"[ERROR] Failed to resolve {domain}.")
        except Exception as e:
            result_label.config(text="Error: An unexpected error occurred.", fg='red')
            print(f"[ERROR] Unexpected error: {e}")

    # Button to check DNS
    check_button = tk.Button(frame, text="Check DNS", bg='black', fg='cyan', font=("Arial", 12), command=check_dns)
    check_button.pack(pady=10)

    # Label to display the result
    result_label = tk.Label(frame, text="", bg='black', fg='white', font=("Arial", 12))
    result_label.pack(pady=10)

    return frame

def create_settings_frame(root):
    frame = tk.Frame(root, bg='black')
    settings_label = tk.Label(frame, text="Framework Information", bg='black', fg='white', font=("Arial", 20, "bold"))
    settings_label.pack(pady=20)

    # Framework Info
    info_frame = tk.Frame(frame, bg='black', bd=1, relief=tk.RAISED)
    info_frame.pack(pady=10, padx=20, fill=tk.X)
    
    # Version info
    version_label = tk.Label(info_frame, text="Version: 1.0.0", bg='black', fg='cyan', font=("Arial", 14))
    version_label.pack(pady=10)
    
    # Author info
    author_label = tk.Label(info_frame, text="Author: Kcyb3r", bg='black', fg='cyan', font=("Arial", 14))
    author_label.pack(pady=10)
    
    # Framework description
    desc_text = """
    Kex Framework is a comprehensive penetration testing toolkit 
    that provides various tools for security testing and assessment.
    
    Features:
    • Multiple security tools integration
    • Easy-to-use interface
    • Tool categorization
    • DNS management
    • Automated installation
    
    GitHub: https://github.com/kcyb3r/kex
    """
    
    desc_label = tk.Label(info_frame, text=desc_text, bg='black', fg='white', font=("Arial", 12), justify=tk.LEFT)
    desc_label.pack(pady=20, padx=20)

    # Update section
    update_frame = tk.Frame(frame, bg='black', bd=1, relief=tk.RAISED)
    update_frame.pack(pady=20, padx=20, fill=tk.X)

    def update_framework():
        try:
            result_label.config(text="Updating Kex Framework...", fg='yellow')
            root.update()
            
            # Get the current directory
            current_dir = os.getcwd()
            
            # First ensure we have the right remote URL
            subprocess.run(['git', 'remote', 'set-url', 'origin', 'https://github.com/Kcyb3r/Kex.git'], 
                         cwd=current_dir,
                         check=True)
            
            # Run git pull to update
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                 cwd=current_dir,
                                 capture_output=True, 
                                 text=True)
            
            if "Already up to date" in result.stdout:
                result_label.config(text="Framework is already up to date!", fg='cyan')
            elif result.returncode == 0:
                result_label.config(text="Framework updated successfully!\nPlease restart Kex.", fg='green')
            else:
                result_label.config(text=f"Update failed: {result.stderr}", fg='red')
                
        except Exception as e:
            result_label.config(text=f"Error during update: {str(e)}", fg='red')
            print(f"[ERROR] Update failed: {e}")

    update_button = tk.Button(update_frame, 
                            text="Update Framework", 
                            bg='black', 
                            fg='cyan',
                            font=("Arial", 12),
                            command=update_framework)
    update_button.pack(pady=10)

    # Label to show update status
    result_label = tk.Label(update_frame, 
                           text="", 
                           bg='black', 
                           fg='white', 
                           font=("Arial", 12))
    result_label.pack(pady=10)

    return frame

def main():
    # Display the banner for Kex Framework using pyfiglet
    banner = pyfiglet.figlet_format("Kex Framework")
    print(banner)

    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, lambda s, f: root.quit())
    signal.signal(signal.SIGTSTP, lambda s, f: root.quit())  # Handle Ctrl+Z

    root = tk.Tk()
    root.title("Kex")  # App name
    root.geometry("500x400")  # Set the window size
    root.configure(bg='black')  # Set background color

    # Create a frame for the sidebar with a black theme, increased width, and a border
    sidebar = tk.Frame(root, bg='black', width=300, height=400, bd=2, relief=tk.RAISED)  # Increased width
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Load and display the logo
    logo_image = Image.open("logo.jpg")  # Load your logo image
    logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Resize as needed
    logo_photo = ImageTk.PhotoImage(logo_image)  # Convert to PhotoImage
    logo_label = tk.Label(sidebar, image=logo_photo, bg='black')  # Create a label for the logo
    logo_label.image = logo_photo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)  # Add some padding

    # Add a separator
    separator = tk.Frame(sidebar, bg='gray', height=2)  # Create a gray separator
    separator.pack(fill=tk.X, pady=5)  # Fill horizontally and add some vertical padding

    # Create frames for each section
    dashboard_frame = create_dashboard_frame(root)
    tools_frame = create_tools_frame(root)
    about_frame = create_about_frame(root)
    dns_frame = create_dns_frame(root)
    settings_frame = create_settings_frame(root)  # Add this line

    # Function to show a specific frame
    def show_frame(frame):
        dashboard_frame.pack_forget()
        tools_frame.pack_forget()
        about_frame.pack_forget()
        dns_frame.pack_forget()
        settings_frame.pack_forget()  # Add this line
        frame.pack(fill=tk.BOTH, expand=True)
        print(f"[LOG] Switched to {frame}.")

    # Add buttons to the sidebar
    dashboard_button = tk.Button(sidebar, text="Dashboard", bg='black', fg='white', font=("Arial", 12, "bold"), bd=0, highlightthickness=0, command=lambda: [show_frame(dashboard_frame), print("[LOG] Clicked Dashboard.")])
    dashboard_button.pack(pady=10)

    tool_button = tk.Button(sidebar, text="Tools", bg='black', fg='white', font=("Arial", 12, "bold"), bd=0, highlightthickness=0, command=lambda: [show_frame(tools_frame), print("[LOG] Clicked Tools.")])
    tool_button.pack(pady=10)

    about_button = tk.Button(sidebar, text="About", bg='black', fg='white', font=("Arial", 12, "bold"), bd=0, highlightthickness=0, command=lambda: [show_frame(about_frame), print("[LOG] Clicked About.")])
    about_button.pack(pady=10)

    # Add DNS button to the sidebar
    dns_button = tk.Button(sidebar, text="DNS", bg='black', fg='white', font=("Arial", 12, "bold"), bd=0, highlightthickness=0, command=lambda: [show_frame(dns_frame), print("[LOG] Clicked DNS.")])
    dns_button.pack(pady=10)

    # Add Settings button to the sidebar
    settings_button = tk.Button(sidebar, text="Settings", bg='black', fg='white', font=("Arial", 12, "bold"), 
                              bd=0, highlightthickness=0, 
                              command=lambda: [show_frame(settings_frame), print("[LOG] Clicked Settings.")])
    settings_button.pack(pady=10)

    # Show the dashboard frame by default
    show_frame(dashboard_frame)

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", root.quit)

    root.mainloop()

if __name__ == "__main__":
    main()
