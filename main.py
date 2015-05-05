import mysql.connector
from mysql.connector import errorcode

try:
    db = mysql.connector.connect(user="root",password="password",host="localhost",database="magic100",buffered=True)

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

name = raw_input('Enter a student name here: ')

cursor = db.cursor()
QUERY = "SELECT student_id,student_name FROM students WHERE student_name = '%s'" % name

cursor.execute(QUERY)
for (id, name) in cursor:
    student_id = id
    student_name = name

#print student_id, student_name

get_unknown_word_ids = "SELECT word_id FROM known_words WHERE student_id = %s" % student_id
cursor.execute(get_unknown_word_ids)
unknown_word_ids = []
for word_id in cursor:
    unknown_word_ids.append(word_id)
#print unknown_word_ids
# query unknown words
unknown_words=[]
for id in unknown_word_ids:
    unknown_words_query = "SELECT word FROM word_list WHERE word_id = %s" % id
    cursor.execute(unknown_words_query)
    for word in cursor:
        unknown_words.append(word)
cursor.close()

print "%s's 5 Unknowns:" % name
for i in range(5):
    print '%s' % unknown_words[i]

# # --SETUP--
#
# #creates all students and their ID's (numbers from 1 to len(students))
# cursor = db.cursor()
# num_students = input("How many students do you have?")
# student_names = []
# while len(student_names) <= num_students:
#     student_names.append(input("Please enter each name, followed by enter: "))
# student_id = 1
# for name in student_names:
#     QUERY = "INSERT into students (student_id,student_name) VALUE (%s,%s)" % (student_id,name)
#     cursor.execute(QUERY)
#     student_id += 1
# db.commit()
# # assumes all words unknown - can be set up correctly later.
# create_list = input("Add in 100 words for all students? 1 for yes, 2 for no: ")
# if create_list == 1:
#     for i in range(1,len(student_names)+1):
#         for j in range(1,101):
#             QUERY = "INSERT into known_words (student_id,word_id) VALUE (%s,%s)" % (i,j)
# db.commit()
# cursor.close()
# db.close()
# # --SETUP COMPLETE--

# -- Remove Known Words --
def return_student_id(name):
    cursor = db.cursor()
    QUERY = "SELECT student_id FROM students WHERE student_name = '%s'" % name
    cursor.execute(QUERY)
    for id in cursor:
        num = id
    cursor.close()
    return num

# name = raw_input("Enter Student Name: ")
# student_id = '%d' % return_student_id(name)
# known_words = raw_input("Enter newly learned words, separated by a comma: ").split(', ')
# cursor = db.cursor()
# known_word_id = []
# for word in known_words:
#     QUERY = "SELECT word_id FROM word_list WHERE word = '%s'" % word
#     cursor.execute(QUERY)
#     for id in cursor:
#         id = '%s' % id
#         known_word_id.append(id)
# cursor.close()
# cursor = db.cursor()
# for id in known_word_id:
#     QUERY = "DELETE FROM known_words WHERE student_id = %s AND word_id = %s" % (student_id,id)
#     cursor.execute(QUERY)
# db.commit()
# cursor.close()



