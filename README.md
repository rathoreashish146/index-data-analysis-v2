# Index-Data-Analysis

A powerful web application for analyzing financial index data with interactive visualizations and comprehensive statistical analysis.

## Features

- **Single Index Analysis**: Analyze one market index in depth with drop/gain event detection, technical indicators, and statistical summaries
- **Cross Index Comparison**: Compare two indexes to understand their relationship, correlation, and relative performance
- **Drawdown & Recovery Analysis**: Identify and analyze market corrections and their recovery patterns
- **Technical Indicators**: RSI, MACD, Bollinger Bands, Moving Averages, and more
- **Weekend-Aware Calculations**: Intelligent handling of weekends for accurate calendar-based analysis

## Project Structure

The project is organized into modular files for better maintainability:

```
Index-Data-Analysis-main/
├── app.py              # Main application file - app initialization and routing
├── layouts.py           # Layout functions (navbar, home, single, cross, docs pages)
├── callbacks.py         # All Dash app callbacks for user interactions
├── components.py        # Reusable UI components (Card, Field, Button, etc.)
├── utils.py             # Utility functions (data processing, calculations, indicators)
├── config.py            # Configuration (CSS styles, constants, store IDs)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### File Descriptions

- **app.py**: Main entry point. Initializes the Dash app, sets up the layout, and registers callbacks.
- **layouts.py**: Contains all page layout functions:
  - `navbar()`: Navigation bar component
  - `home_layout()`: Home page with feature cards
  - `single_layout()`: Single index analysis page
  - `cross_layout()`: Cross index comparison page
  - `docs_layout()`: Documentation page
- **callbacks.py**: All callback functions registered via `register_callbacks(app)`:
  - File upload handlers
  - Analysis execution callbacks
  - UI interaction handlers
  - Drawdown analysis callbacks
- **components.py**: Reusable UI components:
  - `PageContainer`, `Card`, `Field`
  - `RadioGroup`, `CheckboxGroup`
  - `DateRangePicker`, `FileDropzone`, `Button`
- **utils.py**: Data processing and analysis utilities:
  - CSV parsing and validation
  - Date range calculations
  - Weekend-aware return calculations
  - Technical indicator calculations
  - Drawdown recovery analysis
- **config.py**: Application configuration:
  - CSS styles and HTML template (`APP_INDEX_STRING`)
  - Store IDs for data persistence
  - Month options for date pickers

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Index-Data-Analysis-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python app.py
```

The application will start on `http://localhost:8050` (or the port specified by the `PORT` environment variable).

## Data Format

Your CSV file must contain exactly two columns:
1. **Date column**: Any reasonable date format (YYYY-MM-DD, MM/DD/YYYY, etc.)
2. **Numeric column**: Index value (price, level, etc.)

Column headers can have any name - the app automatically detects which is the date and which is numeric.

Example:
```csv
Date,Index
2024-01-01,1000.5
2024-01-02,1005.2
2024-01-03,998.7
```

## Features Overview

### Single Index Analysis
- Upload CSV data
- Configure drop/gain analysis parameters
- View event statistics and probability
- Interactive charts and visualizations
- Technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Drawdown & recovery analysis

### Cross Index Analysis
- Upload two CSV files
- Compare indexes side-by-side
- Correlation analysis
- Relative performance visualization
- Statistical comparison

## Requirements

See `requirements.txt` for the complete list of dependencies. Main dependencies include:
- dash
- pandas
- numpy
- plotly

## License

See LICENSE file for details.
