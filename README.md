# Student Marks Analyzer

A complete Apache Spark-based Big Data project that analyzes student marks data and presents the results in a beautiful college-themed web dashboard.

## Features

- Upload CSV files containing student marks data
- Process data using Apache Spark (PySpark)
- Calculate analytics such as:
  - Highest marks in each subject
  - Overall topper student
  - Subject-wise average marks
  - Overall pass percentage
- Beautiful college-themed dashboard with charts and tables
- Responsive design with academic styling

## Technologies Used

- **Backend**: Python, Flask, PySpark
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, Chart.js
- **Data Processing**: Apache Spark
- **Visualization**: Chart.js for data visualization

## Project Structure

```
Student Marks Analyzer/
│
├── backend/
│   ├── app.py              # Flask web server
│   └── spark_analyzer.py   # Spark data processing logic
│
├── data/
│   └── sample_student_marks.csv  # Sample data for testing
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom college-themed styles
│   ├── js/
│   │   └── main.js         # Frontend JavaScript logic
│   └── images/
│
├── templates/
│   └── index.html          # Main HTML template
│
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Installation

1. **Prerequisites**:
   - Python 3.7 or higher
   - Java 8 or higher (required for Spark)
   - pip (Python package installer)

2. **Clone or Download the Repository**:
   ```
   git clone <repository-url>
   cd SPART-Assignment-2
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. **Start the Web Server**:
   ```
   cd backend
   python app.py
   ```

2. **Access the Application**:
   Open your web browser and navigate to `http://localhost:5000`

3. **Using the Application**:
   - Click "Choose File" to select a CSV file with student marks data
   - Click "Upload CSV" to upload the file
   - Click "Analyze Marks" to process the data
   - View the analytics dashboard with results

## CSV File Format

The application expects a CSV file with the following format:

```
Student Name,Mathematics,Physics,Chemistry,English,Computer Science
Alice Johnson,85,78,92,88,90
Bob Smith,76,85,79,82,87
...
```

- First column should be student names
- Subsequent columns should be subject names with numerical marks
- Missing values are treated as 0

## Analytics Provided

- **Highest Marks**: Shows the highest score achieved in each subject
- **Average Marks**: Displays the class average for each subject
- **Pass Percentage**: Calculates the percentage of students who passed (scored 35 or above) in each subject
- **Class Performance Summary**: Shows overall statistics including:
  - Total number of students
  - Topper student and their total marks
  - Class average marks
  - Number of students passed and failed
  - Overall pass percentage
- **Subject Averages Visualization**: Bar chart showing subject-wise average marks
- **Student Marks Table**: Complete table of all student marks

## Customization

- **Pass Mark**: The default pass mark is 35. To change this, modify the `pass_mark` variable in `backend/spark_analyzer.py`
- **Styling**: Modify `static/css/style.css` to change the college theme colors and styling
- **Additional Subjects**: The application automatically detects subjects from the CSV headers

## Troubleshooting

1. **Java Not Found Error**: Ensure Java is installed and JAVA_HOME is set correctly
2. **Port Already in Use**: Change the port in `backend/app.py` if 5000 is occupied
3. **Large Files**: The application supports files up to 16MB by default

## Sample Data

A sample CSV file is provided in the `data/` directory for testing purposes.

## License

This project is developed for educational purposes as part of a college big data assignment.

---

Made for College Big Data Project by Taniya