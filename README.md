# Job_analyzer
Streamlit-powered dashboard for analyzing tech salary datasets. Features dynamic filtering, automated column mapping, and interactive Plotly visualizations. Includes caching, error handling, and responsive design.
## 🌟 Key Features

### 📊 Dynamic Dashboard
- **Interactive filters** for job titles, countries, and salary ranges
- **Real-time metrics** displaying average salary, median salary, and job count
- **Responsive design** that works on all devices

### 📈 Advanced Visualizations
- **Salary distribution** histogram with experience-level breakdown
- **Box plot analysis** of salaries by experience level
- **Temporal trends** showing salary progression by year (when data available)

### 🔍 Data Exploration
- **Top paying companies** ranking
- **Detailed job listings** with sorting capabilities
- **Smart column detection** that adapts to different dataset formats

## 🛠️ Technical Implementation

### Built With
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly Express** - Interactive visualizations
- **Python 3.8+** - Core programming language

### Smart Data Handling
```python
# Automatic column name detection
column_mapping = {
    'company': 'company_name',
    'employer_name': 'company_name',
    'company_location': 'location'
}
