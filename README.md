# Student Tracking and Career Progress Analysis

## Overview
This tool was made for a company running reskilling or upskilling programs to track student career outcomes. It visualizes how students perform in the job market after completing a course.

## Key Features

- **Data Upload**  
  Upload a `.csv` file with student records. **The file must follow a specific format with predefined column names** based on the company’s internal database.

- **Bar Charts**  
  Visualize data related to:
  - Job found / not found  
  - Career path change  
  - Job relevance to the completed course  

- **Comparison Options**  
  Each chart can group data by:
  - Course name  
  - Funding source  
  - Course completion (with or without certificate)  
  - Participation in the company’s job assistance program  

- **Year Filter**  
  Filter charts by the year the course was completed.

- **Missing Data Overview**  
  Display the percentage of missing values in relevant variables.

## Tech Stack

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Seaborn  
- Matplotlib

## Installation

### Requirements
- Python 3.8+
- `pip` package manager

### Setup
```bash
pip install -r requirements.txt
```

## Running the App
```bash
streamlit run app.py
```
## Usage
1. Upload your .csv file.
2. Select the type of chart.
3. Optionally filter data by year.
4. Review charts and missing data summary.

⚠️ Important: The app only works with data that strictly matches the expected column names and structure. The sample file is provided under the name data.csv

## Author
@ambiwalencja

## License
This project is distributed under the [MIT License](LICENSE).