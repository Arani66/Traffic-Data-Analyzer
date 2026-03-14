# Traffic Data Analyzer & Visualizer 🚦

A Python-based desktop application that processes traffic junction data from CSV files, calculates key metrics, and generates interactive visual histograms using Tkinter.

## Features
* **Robust Input Validation:** Ensures user dates are entered correctly, accounting for leap years and month lengths.
* **Data Processing Pipeline:** Reads raw CSV traffic data and extracts valuable insights, including:
  * Total vehicle counts broken down by type (trucks, electric vehicles, 2-wheelers).
  * Peak traffic hour detection.
  * Speed limit violation tracking.
  * Weather condition correlations.
* **Data Persistence:** Automatically logs processed textual outcomes to a `results.txt` file.
* **Data Visualization:** Uses Tkinter to draw a custom, color-coded dual-bar histogram representing hourly vehicle traffic across different junctions.
* **Batch Processing:** Allows users to continuously process multiple datasets in a single session.

## Technologies Used
* **Python 3**
* **Tkinter** (GUI / Canvas drawing)
* **CSV / OS modules** (File handling)

## Getting Started

### Prerequisites
Ensure you have Python 3 installed on your machine. Tkinter is included with the standard Python library.

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/Traffic-Data-Analyzer.git](https://github.com/yourusername/Traffic-Data-Analyzer.git)