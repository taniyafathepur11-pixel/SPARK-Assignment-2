import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, max, count, when, sum as spark_sum
from pyspark.sql.types import DoubleType
import pandas as pd
import sys
import os

def analyze_student_marks(csv_file_path):
    """
    Analyze student marks using PySpark and return analytics results
    """
    # Validate file existence
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    # Check if file is empty
    if os.path.getsize(csv_file_path) == 0:
        raise ValueError("CSV file is empty")
    
    # Create Spark session with local configuration to avoid Hadoop issues on Windows
    spark = SparkSession.builder \
        .appName("StudentMarksAnalyzer") \
        .config("spark.sql.adaptive.enabled", "false") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "false") \
        .config("spark.hadoop.fs.file.impl", "org.apache.hadoop.fs.LocalFileSystem") \
        .config("spark.hadoop.fs.defaultFS", "file:///") \
        .getOrCreate()
    
    try:
        # Read CSV file
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(csv_file_path)
        
        # Validate that we have data
        if df.isEmpty():
            raise ValueError("CSV file contains no data rows")
        
        # Convert all mark columns to numeric (except student name column)
        student_col = df.columns[0]  # Assuming first column is student name
        mark_columns = [col_name for col_name in df.columns if col_name != student_col]
        
        # Validate that we have mark columns
        if not mark_columns:
            raise ValueError("No subject columns found in CSV file")
        
        # Convert mark columns to numeric and handle missing values
        for mark_col in mark_columns:
            # Replace empty strings with None, then cast to double, then fill None with 0
            df = df.withColumn(mark_col, 
                              when(col(mark_col) == "", None)
                              .otherwise(col(mark_col)))
            df = df.withColumn(mark_col, col(mark_col).cast(DoubleType()))
            df = df.withColumn(mark_col, 
                              when(col(mark_col).isNull(), 0.0)
                              .otherwise(col(mark_col)))
        
        # Calculate subject-wise highest marks
        highest_marks_expr = [max(col_name).alias(f"max_{col_name}") for col_name in mark_columns]
        highest_marks_row = df.agg(*highest_marks_expr).collect()[0]
        highest_marks = {col_name: highest_marks_row[f"max_{col_name}"] for col_name in mark_columns}
        
        # Calculate subject-wise average marks
        avg_marks_expr = [avg(col_name).alias(f"avg_{col_name}") for col_name in mark_columns]
        avg_marks_row = df.agg(*avg_marks_expr).collect()[0]
        avg_marks = {col_name: round(avg_marks_row[f"avg_{col_name}"], 2) for col_name in mark_columns}
        
        # Calculate overall marks for each student (sum of all subjects)
        overall_expr = sum([col(col_name) for col_name in mark_columns])
        df_with_total = df.withColumn("overall_marks", overall_expr)
        
        # Find topper student
        topper_row = df_with_total.orderBy(col("overall_marks").desc()).first()
        topper_student = {
            "name": topper_row[student_col],
            "total_marks": topper_row["overall_marks"]
        }
        
        # Calculate pass/fail statistics (assuming pass mark is 35)
        pass_mark = 35
        
        # Count students who passed in each subject
        pass_count_expr = [count(when(col(col_name) >= pass_mark, True)).alias(f"pass_{col_name}") for col_name in mark_columns]
        pass_count_row = df.agg(*pass_count_expr).collect()[0]
        pass_counts = {col_name: pass_count_row[f"pass_{col_name}"] for col_name in mark_columns}
        
        # Calculate total students
        total_students = df.count()
        
        # Calculate pass percentage for each subject
        pass_percentages = {col_name: round((pass_counts[col_name] / total_students) * 100, 2) 
                           for col_name in mark_columns}
        
        # Calculate overall class average
        class_avg = df_with_total.agg(avg("overall_marks")).collect()[0][0]
        class_avg = round(class_avg, 2)
        
        # Count total students passed (students who scored >= 35 in ALL subjects)
        df_passed = df_with_total
        for col_name in mark_columns:
            df_passed = df_passed.filter(col(col_name) >= pass_mark)
        
        total_passed = df_passed.count()
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
            "raw_data": df.toPandas().to_dict('records')  # Convert to dict for JSON serialization
        }
        
        return results
    
    except Exception as e:
        raise Exception(f"Error in analyzing student marks: {str(e)}")
    
    finally:
        # Stop Spark session
        spark.stop()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python spark_analyzer.py <csv_file_path>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    results = analyze_student_marks(csv_file_path)
    print(results)