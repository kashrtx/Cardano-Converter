# Cardano Converter

A modern, elegant Tkinter application for converting between Cardano (ADA) cryptocurrency and Canadian Dollars (CAD), featuring an Apple-inspired design.

<img src="https://res.coinpaper.com/coinpaper/cardano_ada_logo_d684df0304.png" width="200" title="Cardano Logo" alt="Cardano Logo"/>

## Features

- **Real-time Conversion**: Uses live Cardano price data with multiple data sources and fallbacks
- **Interactive Price Chart**: Visual representation of price changes over time
- **Bidirectional Conversion**: Convert from CAD to ADA and vice versa
- **Premium UI**: Apple-inspired interface with smooth animations, rounded corners, and a clean layout
- **Live Updates**: Price updates automatically every 30 seconds
- **Responsive Interface**: Clear visual feedback during conversions
- **Cryptocurrency Stats**: View market data including market cap, volume, and supply
- **Split Panel Design**: Conversion tools on one side with information and charts on the other

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/cardano-converter.git
   cd cardano-converter
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python cardano_converter.py
   ```

## Requirements

- Python 3.6 or higher
- Required packages:
  - tkinter (usually comes with Python)
  - customtkinter (for modern UI components)
  - matplotlib (for price charts)
  - requests
  - beautifulsoup4
  - Pillow (for image processing)

## How to Use

1. Launch the application using `python cardano_converter.py`
2. Enter the amount you want to convert in the input field
3. Click either:
   - "Convert CAD to ADA" to convert Canadian Dollars to Cardano
   - "Convert ADA to CAD" to convert Cardano to Canadian Dollars
4. View your conversion result in the output box
5. See the price chart update in real-time every 30 seconds
6. Click "Clear" to reset the input and start a new conversion

## UI Features

- **Price Chart**: Visual representation of ADA price changes
- **Cryptocurrency Information**: At-a-glance market statistics 
- **Modern Controls**: Sleek buttons, text boxes, and cards with subtle shadows
- **Animated Feedback**: Visual cues when conversions occur
- **Apple-Inspired Design**: Clean typography, carefully chosen colors, and iOS-like visual elements

## About

This application was developed by Kaushal Bhingaradia. The current version is a modern Tkinter reimplementation of an earlier Kivy-based application. The UI has been completely redesigned to provide an elegant, Apple-inspired experience.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Cardano blockchain and community
- Python Tkinter and customtkinter communities
- Original ada_logo.png by Cardano Foundation
