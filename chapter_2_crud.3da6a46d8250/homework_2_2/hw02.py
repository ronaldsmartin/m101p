import pymongo
import sys

# Connect to the database.
connection = pymongo.MongoClient("mongodb://localhost")

db = connection.students
grades = db.grades

# Find IDs and scores for homework documents.
hw_query = {"type": "homework"}
selector = {"student_id":1, "score": 1}
homework = grades.find(hw_query, selector)

# Sort by student_id and then by homework.
homework = homework.sort( [ ("student_id", pymongo.ASCENDING), ("score", pymongo.DESCENDING) ] )

# Remove minima using the hint.
last_doc = homework[0]
last_student_id = last_doc["student_id"]

for doc in homework:
  student_id = doc["student_id"]

  # When the student_id changes between entries, we know the previous item was a minimum.
  if last_student_id != student_id:
    try:
      print "Removing ", last_doc
      grades.remove(last_doc)
    except:
      print "Exception while removing ", last_doc

  last_doc = doc
  last_student_id = student_id

# The last element in the sorted list is a minimum that is undetected by the hint's strategy.
try:
  print "Removing ", last_doc
  grades.remove(last_doc)
except:
  print "Exception while removing ", last_doc
