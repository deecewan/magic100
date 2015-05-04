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
QUERY = "SELECT studentid,studentname FROM students WHERE studentname = '%s'" % name

cursor.execute(QUERY)
for (studentid,studentname) in cursor:
    student_id = studentid
    student_name = studentname

#print student_id, student_name
cursor.close()
cursor = db.cursor()
get_unknown_word_ids = "SELECT word_id FROM known_words WHERE student_id = %s" %student_id
cursor.execute(get_unknown_word_ids)
unknown_word_ids = []
for word_id in cursor:
    unknown_word_ids.append(word_id)
#print unknown_word_ids
cursor.close()
# query unknown words
cursor = db.cursor()
unknown_words=[]
for id in unknown_word_ids:
    unknown_words_query = "SELECT word FROM word_list WHERE word_id = %s" % id
    cursor.execute(unknown_words_query)
    for word in cursor:
        unknown_words.append(word)
cursor.close()

print "%s's 5 Unknowns:" % student_name
for i in range(5):
    print '%s' % unknown_words[i]


# cursor = db.cursor()

# for i in range(1,24):
#     for j in range(1,33):
#         QUERY = "INSERT into known_words (student_id,word_id) VALUE (%s,%s)" % (i,j)
#         print QUERY
#         cursor.execute(QUERY)
# db.commit()
# cursor.close()




db.close()