import pandas as pd
import mysql.connector

# Load CSV data into a DataFrame
df = pd.read_csv('/Users/apple/downloads/Student_performance_data_.csv')

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='todos'
)

cursor = conn.cursor()

# Insert DataFrame records one by one
for i, row in df.iterrows():
    sql = ("INSERT INTO students (StudentID,Age,Gender,Ethnicity,ParentalEducation,StudyTimeWeekly,Absences,Tutoring,ParentalSupport,Extracurricular,Sports,Music,Volunteering,GPA,GradeClass) "
           "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(sql, tuple(row))

conn.commit()
cursor.close()
conn.close()
