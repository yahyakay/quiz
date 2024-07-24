import pandas as pd
import os
import glob
import mysql.connector


# # Load CSV data into a DataFrame
# df = pd.('/Users/apple/OpenTriviaQA')

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='quiz_db'
)

cursor = conn.cursor()

# use glob to get all the csv files
# in the folder
path = "/Users/apple/Documents/OpenTriviaQA/categories"
csv_files = glob.glob(os.path.join(path, "*"))

# loop over the list of csv files
for f in csv_files:
    print('Location:', f)
    print('File Name:', f.split("\\")[-1])
    filename=f.split("/")[-1]
    # Insert DataFrame records one by one
    sql = "INSERT INTO categories (name) VALUES ('"+ filename +"')"
    cursor.execute(sql)
    categoryId=cursor.lastrowid

    # read the csv file

    # Using readlines()
    file1 = open(f, 'r', encoding='latin-1')
    Lines = file1.readlines()
    #
    count = 0

    question = ""
    answer = ""
    choice1 = ""
    choice2 = ""
    choice3 = ""
    choice4 = ""
    # # Strips the newline character
    for line in Lines:
        if len(line.strip()) != 0:
            print("here " +line)
            if line.startswith("#"):
                question = line.replace('\n', '')
            if line.startswith("^"):
                answer = line.replace('\n', '')
            if line.startswith("A"):
                choice1 = line.replace('\n', '')
            if line.startswith("B"):
                choice2 = line.replace('\n', '')
            if line.startswith("C"):
                choice3 = line.replace('\n', '')
            if line.startswith("D"):
                choice4 = line.replace('\n', '')
            print( question + "','" + answer + "','" + choice1 + "','" + choice2 + "','" + choice3 + "','" + choice4 + "'," + str(categoryId)  )

        else:
            sql = ("INSERT INTO questions (question,answer,choice1,choice2,choice3,choice4,category_id) "
               "VALUES ('" + question + "','" + answer + "','" + choice1 + "','" + choice2 + "','" + choice3 + "','" + choice4 + "'," + str(categoryId) + ")")
            cursor.execute(sql)
            print(sql)


conn.commit()
cursor.close()
conn.close()

