import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import time
from PIL import Image, ImageTk
import os
import io
import sys
import webbrowser
import json
import re
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import random

# Set customtkinter appearance
ctk.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class CardanoConverter:
    def __init__(self, root):
        # Root window configuration
        self.root = root
        self.root.title("Cardano Converter")
        self.root.geometry("900x980")
        self.root.configure(bg="#f5f5f7")
        self.root.resizable(False, False)
        
        # Set app icon if available
        try:
            self.icon = Image.open("ada_logo.png")
            self.icon = ImageTk.PhotoImage(self.icon)
            self.root.iconphoto(True, self.icon)
        except:
            pass

        # Colors - Apple inspired
        self.dark_blue = "#007AFF"  # Apple blue
        self.light_blue = "#5AC8FA" # Light blue
        self.accent = "#FF2D55"     # Accent pink
        self.text_color = "#1D1D1F" # Dark gray
        self.bg_color = "#f5f5f7"   # Light gray background
        self.card_bg = "#FFFFFF"    # White for cards
        self.success_green = "#34C759" # Apple success green
        
        # Counter for conversions
        self.count = 0
        
        # Historical price data for chart
        self.price_history = []
        self.time_history = []
        
        # Create custom fonts
        self.create_fonts()
        
        # Current price storage
        self.current_price = "0.00"
        
        # Build the UI
        self.create_ui()
        
        # Start price update thread
        self.update_price()
        self.start_price_thread()

    def create_fonts(self):
        """Create custom fonts for the application"""
        # Use CTkFont for customtkinter compatibility
        self.title_font = ctk.CTkFont(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = ctk.CTkFont(family="Helvetica", size=20, weight="bold")
        self.price_font = ctk.CTkFont(family="Helvetica", size=34, weight="bold")
        self.button_font = ctk.CTkFont(family="Helvetica", size=14, weight="bold")
        self.result_font = ctk.CTkFont(family="Helvetica", size=26, weight="bold")
        self.small_font = ctk.CTkFont(family="Helvetica", size=12)
        self.tiny_font = ctk.CTkFont(family="Helvetica", size=10)
        
        # For tkinter widgets that don't accept CTkFont
        self.tk_title_font = (("Helvetica"), 24, "bold")
        self.tk_subtitle_font = (("Helvetica"), 16)
        self.tk_small_font = (("Helvetica"), 12)
        self.tk_tiny_font = (("Helvetica"), 10)
    
    def create_ui(self):
        """Create the main user interface"""
        # Main container with left and right panes
        self.main_container = tk.Frame(self.root, bg=self.bg_color)
        self.main_container.pack(fill="both", expand=True)
        
        # Left pane (conversion tools)
        self.left_pane = tk.Frame(self.main_container, bg=self.bg_color, width=400)
        self.left_pane.pack(side="left", fill="both", padx=20, pady=20)
        
        # Right pane (price chart and info)
        self.right_pane = tk.Frame(self.main_container, bg=self.bg_color, width=400)
        self.right_pane.pack(side="right", fill="both", padx=20, pady=20)
        
        # Configure the panes to maintain their widths
        self.left_pane.pack_propagate(False)
        self.right_pane.pack_propagate(False)
        
        # Create components for left pane
        self.create_left_pane()
        
        # Create components for right pane
        self.create_right_pane()
        
    def create_left_pane(self):
        """Create the left pane with conversion tools"""
        # Logo and Title section
        self.header_frame = tk.Frame(self.left_pane, bg=self.bg_color)
        self.header_frame.pack(fill="x", pady=(0, 15))
        
        # Logo
        try:
            logo_img = Image.open("ada_logo.png")
            logo_img = logo_img.resize((60, 60), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            self.logo_label = tk.Label(self.header_frame, image=self.logo, bg=self.bg_color)
            self.logo_label.pack(side="left", padx=(0, 10))
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Title and subtitle in vertical layout
        self.title_frame = tk.Frame(self.header_frame, bg=self.bg_color)
        self.title_frame.pack(side="left", fill="y")
        
        self.title_label = tk.Label(
            self.title_frame,
            text="Cardano Converter",
            font=self.tk_title_font,
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        self.title_label.pack(fill="x", anchor="w")
        
        self.subtitle_label = tk.Label(
            self.title_frame,
            text="ADA ⟷ CAD",
            font=self.tk_subtitle_font,
            bg=self.bg_color,
            fg=self.text_color,
            anchor="w"
        )
        self.subtitle_label.pack(fill="x", anchor="w")
        
        # Price card with shadow effect
        self.price_container = tk.Frame(self.left_pane, bg="#DDDDDD", padx=2, pady=2)
        self.price_container.pack(fill="x", pady=15)
        
        self.price_frame = ctk.CTkFrame(
            self.price_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.price_frame.pack(fill="x", padx=1, pady=1)
        
        self.price_label = ctk.CTkLabel(
            self.price_frame,
            text="Current Price",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.price_label.pack(pady=(15, 5))
        
        self.price_value = ctk.CTkLabel(
            self.price_frame,
            text="$0.00 CAD",
            font=self.price_font,
            text_color=self.dark_blue,
            fg_color="transparent"
        )
        self.price_value.pack(pady=5)
        
        self.price_time = ctk.CTkLabel(
            self.price_frame,
            text=f"Last updated: {self.get_date_time()}",
            font=self.tiny_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.price_time.pack(pady=(5, 15))
        
        # Conversion card with shadow effect
        self.conversion_container = tk.Frame(self.left_pane, bg="#DDDDDD", padx=2, pady=2)
        self.conversion_container.pack(fill="x", pady=15)
        
        self.conversion_frame = ctk.CTkFrame(
            self.conversion_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.conversion_frame.pack(fill="x", padx=1, pady=1)
        
        self.conversion_label = ctk.CTkLabel(
            self.conversion_frame,
            text="Enter Amount to Convert",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.conversion_label.pack(pady=(15, 10))
        
        # Input with modern styling
        self.input_var = tk.StringVar(value="0")
        self.input_entry = ctk.CTkEntry(
            self.conversion_frame,
            textvariable=self.input_var,
            font=self.subtitle_font,
            width=250,
            height=45,
            corner_radius=10,
            border_width=0,
            fg_color="#F2F2F7",
            text_color=self.text_color,
            placeholder_text="Enter amount",
            justify="center"
        )
        self.input_entry.pack(pady=10)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(
            self.conversion_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.button_frame.pack(pady=10)
        
        # CAD to ADA button
        self.cad_to_ada_button = ctk.CTkButton(
            self.button_frame,
            text="Convert CAD to ADA",
            font=self.button_font,
            fg_color=self.dark_blue,
            text_color="white",
            hover_color=self.light_blue,
            corner_radius=10,
            width=250,
            height=40,
            command=self.cad_to_ada
        )
        self.cad_to_ada_button.pack(pady=5)
        
        # ADA to CAD button
        self.ada_to_cad_button = ctk.CTkButton(
            self.button_frame,
            text="Convert ADA to CAD",
            font=self.button_font,
            fg_color=self.dark_blue,
            text_color="white",
            hover_color=self.light_blue,
            corner_radius=10,
            width=250,
            height=40,
            command=self.ada_to_cad
        )
        self.ada_to_cad_button.pack(pady=5)
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame,
            text="Clear",
            font=self.small_font,
            fg_color="#E5E5EA",
            text_color=self.text_color,
            hover_color="#D1D1D6",
            corner_radius=8,
            width=120,
            height=30,
            command=self.clear
        )
        self.clear_button.pack(pady=(0, 10))
        
        # Output Box with shadow effect
        self.output_container = tk.Frame(self.left_pane, bg="#DDDDDD", padx=2, pady=2)
        self.output_container.pack(fill="x", pady=15)
        
        self.output_frame = ctk.CTkFrame(
            self.output_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.output_frame.pack(fill="x", padx=1, pady=1)
        
        self.output_label = ctk.CTkLabel(
            self.output_frame,
            text="Conversion Result",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.output_label.pack(pady=(15, 10))
        
        # Text box for displaying results
        self.output_box = ctk.CTkTextbox(
            self.output_frame,
            width=400,
            height=80,
            corner_radius=10,
            border_width=0,
            fg_color="#F2F2F7",
            text_color=self.dark_blue,
            font=self.result_font,
            activate_scrollbars=False
        )
        self.output_box.pack(pady=10, padx=20)
        self.output_box.insert("1.0", "Enter amount and convert!")
        self.output_box.configure(state="disabled")

        
        self.conversion_count = ctk.CTkLabel(
            self.output_frame,
            text="Conversions: 0",
            font=self.tiny_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.conversion_count.pack(pady=(0, 15))
        
        # Footer
        current_year = datetime.now().year
        self.footer = ctk.CTkLabel(
            self.left_pane,
            text=f"© {current_year} Kaushal Bhingaradia",
            font=self.tiny_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.footer.pack(side="bottom", pady=10)
        
    def create_right_pane(self):
        """Create the right pane with price chart and info"""
        # Chart title
        self.chart_title = ctk.CTkLabel(
            self.right_pane,
            text="Cardano Price Trend",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.chart_title.pack(pady=(0, 10), anchor="w")
        
        # Chart container with shadow effect
        self.chart_container = tk.Frame(self.right_pane, bg="#DDDDDD", padx=2, pady=2)
        self.chart_container.pack(fill="x", pady=10)
        
        self.chart_frame = ctk.CTkFrame(
            self.chart_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.chart_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        # Create initial chart
        self.create_price_chart()
        
        # Stats container with shadow effect
        self.stats_container = tk.Frame(self.right_pane, bg="#DDDDDD", padx=2, pady=2)
        self.stats_container.pack(fill="x", pady=15)
        
        self.stats_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.stats_frame.pack(fill="x", padx=1, pady=1)
        
        self.stats_title = ctk.CTkLabel(
            self.stats_frame,
            text="Cardano Stats",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.stats_title.pack(pady=(15, 10))
        
        # Stats grid
        self.stats_grid = ctk.CTkFrame(
            self.stats_frame,
            fg_color="transparent",
        )
        self.stats_grid.pack(pady=(0, 15), padx=20, fill="x")
        
        # Market Cap
        self.market_cap_label = ctk.CTkLabel(
            self.stats_grid,
            text="Market Cap:",
            font=self.small_font,
            text_color=self.text_color,
            fg_color="transparent",
            anchor="w"
        )
        self.market_cap_label.grid(row=0, column=0, sticky="w", pady=5)
        
        self.market_cap_value = ctk.CTkLabel(
            self.stats_grid,
            text="$11.2B",
            font=self.small_font,
            text_color=self.dark_blue,
            fg_color="transparent",
            anchor="e"
        )
        self.market_cap_value.grid(row=0, column=1, sticky="e", pady=5)
        
        # Volume
        self.volume_label = ctk.CTkLabel(
            self.stats_grid,
            text="24h Volume:",
            font=self.small_font,
            text_color=self.text_color,
            fg_color="transparent",
            anchor="w"
        )
        self.volume_label.grid(row=1, column=0, sticky="w", pady=5)
        
        self.volume_value = ctk.CTkLabel(
            self.stats_grid,
            text="$245.1M",
            font=self.small_font,
            text_color=self.dark_blue,
            fg_color="transparent",
            anchor="e"
        )
        self.volume_value.grid(row=1, column=1, sticky="e", pady=5)
        
        # Circulating Supply
        self.supply_label = ctk.CTkLabel(
            self.stats_grid,
            text="Circulating Supply:",
            font=self.small_font,
            text_color=self.text_color,
            fg_color="transparent",
            anchor="w"
        )
        self.supply_label.grid(row=2, column=0, sticky="w", pady=5)
        
        self.supply_value = ctk.CTkLabel(
            self.stats_grid,
            text="35.4B ADA",
            font=self.small_font,
            text_color=self.dark_blue,
            fg_color="transparent",
            anchor="e"
        )
        self.supply_value.grid(row=2, column=1, sticky="e", pady=5)
        
        # Max Supply
        self.max_supply_label = ctk.CTkLabel(
            self.stats_grid,
            text="Max Supply:",
            font=self.small_font,
            text_color=self.text_color,
            fg_color="transparent",
            anchor="w"
        )
        self.max_supply_label.grid(row=3, column=0, sticky="w", pady=5)
        
        self.max_supply_value = ctk.CTkLabel(
            self.stats_grid,
            text="45B ADA",
            font=self.small_font,
            text_color=self.dark_blue,
            fg_color="transparent",
            anchor="e"
        )
        self.max_supply_value.grid(row=3, column=1, sticky="e", pady=5)
        
        # Configure grid columns
        self.stats_grid.columnconfigure(0, weight=1)
        self.stats_grid.columnconfigure(1, weight=1)
        
        # Info card
        self.info_container = tk.Frame(self.right_pane, bg="#DDDDDD", padx=2, pady=2)
        self.info_container.pack(fill="x", pady=15)
        
        self.info_frame = ctk.CTkFrame(
            self.info_container,
            fg_color=self.card_bg,
            corner_radius=15,
            border_width=0
        )
        self.info_frame.pack(fill="x", padx=1, pady=1)
        
        self.info_title = ctk.CTkLabel(
            self.info_frame,
            text="About Cardano",
            font=self.subtitle_font,
            text_color=self.text_color,
            fg_color="transparent"
        )
        self.info_title.pack(pady=(15, 10))
        
        self.info_text = ctk.CTkTextbox(
            self.info_frame,
            width=350,
            height=120,
            corner_radius=10,
            border_width=0,
            fg_color="#F2F2F7",
            text_color=self.text_color,
            font=self.small_font,
            activate_scrollbars=False
        )
        self.info_text.pack(pady=10, padx=20)
        self.info_text.insert("1.0", "Cardano (ADA) is a proof-of-stake blockchain platform that says its goal is to allow 'changemakers, innovators and visionaries' to bring about positive global change.\n\nThe open-source project also aims to 'redistribute power from unaccountable structures to the margins to individuals' – helping to create a society that is more secure, transparent and fair.")
        self.info_text.configure(state="disabled")
        
        # Open website button
        self.website_button = ctk.CTkButton(
            self.info_frame,
            text="Visit Cardano.org",
            font=self.small_font,
            fg_color=self.dark_blue,
            text_color="white",
            hover_color=self.light_blue,
            corner_radius=8,
            width=150,
            height=30,
            command=lambda: webbrowser.open("https://cardano.org")
        )
        self.website_button.pack(pady=(0, 15))
        
    def create_price_chart(self):
        """Create price chart with matplotlib"""
        # If we already have a chart, clear the frame first
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Create figure
        fig = Figure(figsize=(4, 3), dpi=100)
        fig.patch.set_facecolor('#FFFFFF')
        
        # Adjust the subplot params to make more room for the plot
        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        
        # Add subplot
        plot = fig.add_subplot(111)
        
        # If we have price history, plot it
        if len(self.price_history) > 1:
            # Create x values (number of data points)
            x_values = list(range(len(self.price_history)))
            
            # Plot the price history
            plot.plot(x_values, self.price_history, color=self.dark_blue, linewidth=2)
            
            # Add a subtle fill below the line
            plot.fill_between(x_values, self.price_history, color=self.light_blue, alpha=0.2)
            
            # Set the labels for x-axis ticks (time)
            if len(self.time_history) > 0:
                # Show only a reasonable number of labels to avoid crowding
                max_labels = 5
                step_size = max(1, len(self.time_history) // max_labels)
                
                # Get indices for the labels
                indices = list(range(0, len(self.time_history), step_size))
                
                # If the last point isn't included, add it
                if len(self.time_history) - 1 not in indices:
                    indices.append(len(self.time_history) - 1)
                
                # Convert datetime strings to more readable format
                formatted_times = []
                for i in indices:
                    if i < len(self.time_history):
                        try:
                            dt = datetime.strptime(self.time_history[i], '%Y/%m/%d %I:%M:%S %p')
                            formatted_times.append(dt.strftime('%H:%M'))
                        except:
                            formatted_times.append('')
                
                plot.set_xticks([i for i in indices if i < len(x_values)])
                plot.set_xticklabels(formatted_times)
        else:
            # If no data yet, show a placeholder message
            plot.text(0.5, 0.5, 'Price data will appear here', 
                     horizontalalignment='center', verticalalignment='center',
                     transform=plot.transAxes)
            
        # Style the plot to match the app
        plot.spines['top'].set_visible(False)
        plot.spines['right'].set_visible(False)
        plot.spines['bottom'].set_color('#CCCCCC')
        plot.spines['left'].set_color('#CCCCCC')
        
        plot.tick_params(axis='both', colors='#1D1D1F', labelsize=8)
        plot.grid(axis='y', linestyle='--', alpha=0.3)
        
        plot.set_title('ADA Price (CAD)', fontsize=10, color='#1D1D1F')
        
        # Set y-axis to start from 0 or slightly lower than the min price
        if len(self.price_history) > 0:
            min_price = min(self.price_history)
            max_price = max(self.price_history)
            y_min = max(0, min_price * 0.9)  # Start at 0 or 90% of min price
            y_max = max_price * 1.1  # Go to 110% of max price
            plot.set_ylim(y_min, y_max)
        
        # Create the canvas
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
    def get_date_time(self):
        """Get current formatted date and time"""
        now = datetime.now()
        return now.strftime('%Y/%m/%d %I:%M:%S %p')
    
    def get_realtime_cardano_price(self):
        """Get real-time Cardano price from multiple sources with fallbacks"""
        # Try multiple methods to get the price
        price = self.get_price_from_google()
        
        if not price or price == "0.00":
            price = self.get_price_from_api()
            
        if not price or price == "0.00":
            price = self.get_price_from_coingecko()
            
        if not price or price == "0.00":
            return self.current_price
            
        return price
        
    def get_price_from_google(self):
        """Get price from Google search"""
        try:
            url = "https://www.google.ca/search?q=ADA+to+CAD"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Method 1: Try to find the price element
                price_element = soup.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'})
                if price_element:
                    text = price_element.find("div", attrs={'class': 'BNeawe iBp4i AP7Wnd'})
                    if text:
                        price_text = text.text
                        # Extract numbers using regex
                        match = re.search(r'\d+\.\d+', price_text)
                        if match:
                            return match.group(0)
                
                # Method 2: Alternative class
                price_element = soup.select_one(".DFlfde.SwHCTb")
                if price_element:
                    return price_element.text
                    
                # Method 3: Look for specific pattern
                for div in soup.find_all('div'):
                    if div.text and 'CAD' in div.text and '$' in div.text:
                        match = re.search(r'\$(\d+\.\d+)', div.text)
                        if match:
                            return match.group(1)
            
            return None
        except Exception as e:
            print(f"Error fetching price from Google: {e}")
            return None
            
    def get_price_from_api(self):
        """Get price from CoinGecko API"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=cardano&vs_currencies=cad"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'cardano' in data and 'cad' in data['cardano']:
                    return str(data['cardano']['cad'])
            
            return None
        except Exception as e:
            print(f"Error fetching price from CoinGecko API: {e}")
            return None
            
    def get_price_from_coingecko(self):
        """Get price from CoinGecko website as fallback"""
        try:
            url = "https://www.coingecko.com/en/coins/cardano"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Try to find the price in CAD
                for span in soup.find_all('span'):
                    if 'C$' in span.text:
                        match = re.search(r'C\$(\d+\.\d+)', span.text)
                        if match:
                            return match.group(1)
            
            return None
        except Exception as e:
            print(f"Error fetching price from CoinGecko website: {e}")
            return None
    
    def update_price(self):
        """Update the displayed price and chart data"""
        price = self.get_realtime_cardano_price()
        if price:
            self.current_price = price
            self.price_value.configure(text=f"${price} CAD")
            self.price_time.configure(text=f"Last updated: {self.get_date_time()}")
            
            # Update price history for the chart
            try:
                price_float = float(price)
                self.price_history.append(price_float)
                self.time_history.append(self.get_date_time())
                
                # Keep only the last 24 data points (2 hours if updating every 5 minutes)
                if len(self.price_history) > 24:
                    self.price_history.pop(0)
                    self.time_history.pop(0)
                
                # Update chart if we have at least 2 data points
                if len(self.price_history) >= 2:
                    self.create_price_chart()
            except ValueError:
                pass  # Skip chart update if price isn't a valid float
    
    def start_price_thread(self):
        """Start a thread to update price periodically"""
        def price_updater():
            while True:
                try:
                    # Update the price display and chart
                    self.update_price()
                    
                    # Update stats with some randomized data for demo purposes
                    # In a real app, you'd fetch actual data
                    self.update_stats()
                except Exception as e:
                    print(f"Error in price update thread: {e}")
                
                # Sleep for 30 seconds before next update
                time.sleep(30)
        
        thread = threading.Thread(target=price_updater, daemon=True)
        thread.start()
    
    def update_stats(self):
        """Update cryptocurrency stats with demo data"""
        # In a real application, you would fetch this data from an API
        # Here we're just using random variations for demonstration
        
        try:
            # Market cap: base 11.2B with ±5% variation
            market_cap = 11.2 + (random.random() * 1.12 - 0.56)  # ±5% variation
            self.market_cap_value.configure(text=f"${market_cap:.1f}B")
            
            # Volume: base 245.1M with ±10% variation
            volume = 245.1 + (random.random() * 49.02 - 24.51)  # ±10% variation
            self.volume_value.configure(text=f"${volume:.1f}M")
            
            # Circulating supply: base 35.4B with very small variation
            supply = 35.4 + (random.random() * 0.1 - 0.05)  # very small variation
            self.supply_value.configure(text=f"{supply:.1f}B ADA")
        except Exception as e:
            print(f"Error updating stats: {e}")
    
    def cad_to_ada(self):
        """Convert CAD to ADA"""
        try:
            # Count conversions
            self.count += 1
            
            # Get values
            cad = float(self.input_var.get() or 0)
            cardano_price = float(self.current_price)
            
            # Calculate conversion
            ada = cad / cardano_price
            
            # Update result
            self.update_output_box(f"{cad:.2f} CAD → {ada:.2f} ADA", self.dark_blue)
            self.conversion_count.configure(text=f"Conversions: {self.count}")
            
            # Add a subtle animation flash for the output box
            self.flash_output_box()
        except ValueError:
            self.update_output_box("Please enter a valid number", self.accent)
    
    def ada_to_cad(self):
        """Convert ADA to CAD"""
        try:
            # Count conversions
            self.count += 1
            
            # Get values
            ada = float(self.input_var.get() or 0)
            cardano_price = float(self.current_price)
            
            # Calculate conversion
            cad = ada * cardano_price
            
            # Update result
            self.update_output_box(f"{ada:.2f} ADA → {cad:.2f} CAD", self.dark_blue)
            self.conversion_count.configure(text=f"Conversions: {self.count}")
            
            # Add a subtle animation flash for the output box
            self.flash_output_box()
        except ValueError:
            self.update_output_box("Please enter a valid number", self.accent)
    
    def update_output_box(self, text, color):
        """Update the output text box with given text and color"""
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(text_color=color, state="disabled")
    
    def flash_output_box(self):
        """Create a subtle flash animation for the output box"""
        original_color = self.output_box.cget("fg_color")
        
        # Function to change color back and forth
        def change_color(color, remaining):
            if remaining > 0:
                self.output_box.configure(fg_color=color)
                next_color = original_color if color != original_color else "#E8F1FF"
                self.root.after(100, lambda: change_color(next_color, remaining - 1))
            else:
                self.output_box.configure(fg_color=original_color)
        
        # Start the flash with a light blue color
        change_color("#E8F1FF", 4)  # Flash 4 times
    
    def clear(self):
        """Clear the input and reset the result"""
        self.input_var.set("0")
        self.update_output_box("Enter an amount and press convert", self.text_color)

def main():
    root = tk.Tk()
    app = CardanoConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main() 