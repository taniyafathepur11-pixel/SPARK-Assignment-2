import pandas as pd
import numpy as np
import os

def analyze_student_marks_simple(csv_file_path):
    """
    Simple analyzer using pandas as a fallback when Spark is not available
    """
    # Validate file existence
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Check if file is empty
    if os.path.getsize(csv_file_path) == 0:
        raise ValueError("CSV file is empty")
    
    # Read CSV file
    df = pd.read_csv(csv_file_path)
    
    # Validate that we have data
    if df.empty:
        raise ValueError("CSV file contains no data rows")
    
    # Get student name column (first column)
    student_col = df.columns[0]
    mark_columns = [col_name for col_name in df.columns if col_name != student_col]
    
    # Validate that we have mark columns
    if not mark_columns:
        raise ValueError("No subject columns found in CSV file")
    
    # Convert mark columns to numeric and handle missing values
    for mark_col in mark_columns:
        df[mark_col] = pd.to_numeric(df[mark_col], errors='coerce')
        df[mark_col] = df[mark_col].fillna(0)
    
    # Calculate subject-wise highest marks
    highest_marks = {col_name: float(df[col_name].max()) for col_name in mark_columns}
    
    # Calculate subject-wise average marks
    avg_marks = {col_name: round(float(df[col_name].mean()), 2) for col_name in mark_columns}
    
    # Calculate overall marks for each student (sum of all subjects)
    df['overall_marks'] = df[mark_columns].sum(axis=1)
    
    # Find topper student
    topper_idx = df['overall_marks'].idxmax()
    topper_student = {
        "name": df.loc[topper_idx, student_col],
        "total_marks": float(df.loc[topper_idx, 'overall_marks'])
    }
    
    # Calculate pass/fail statistics (assuming pass mark is 35)
    pass_mark = 35
    
    # Count students who passed in each subject
    pass_counts = {col_name: int((df[col_name] >= pass_mark).sum()) for col_name in mark_columns}
    
    # Calculate total students
    total_students = len(df)
    
    # Calculate pass percentage for each subject
    pass_percentages = {col_name: round((pass_counts[col_name] / total_students) * 100, 2) 
                       for col_name in mark_columns}
    
    # Calculate overall class average
    class_avg = round(float(df['overall_marks'].mean()), 2)
    
    # Count total students passed (students who scored >= 35 in ALL subjects)
    df_passed = df.copy()
    for col_name in mark_columns:
        df_passed = df_passed[df_passed[col_name] >= pass_mark]
    
    total_passed = len(df_passed)
    total_failed = total_students - total_passed
    overall_pass_percentage = round((total_passed / total_students) * 100, 2)
    
    # Prepare results
    results = {
        "total_students": total_students,
        "subject_wise_highest": highest_marks,
        "subject_wise_average": avg_marks,
        "subject_wise_pass_percentage": pass_percentages,
        "topper_student": topper_student,
        "class_average": class_avg,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "overall_pass_percentage": overall_pass_percentage,
        "raw_data": df.to_dict('records')  # Convert to dict for JSON serialization
    }
    
    return results