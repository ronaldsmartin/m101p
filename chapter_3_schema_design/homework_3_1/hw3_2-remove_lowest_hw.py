import pymongo
import sys

## Iterate over a collection of students with scores,
## finding the lowest homework score and removing it.

def find_lowest_homework(scores):
  lowest_hw = None
  lowest_hw_score = 101

  for score in scores:
    points = score["score"]

    if score["type"] == "homework" and points < lowest_hw_score:
      lowest_hw = score
      lowest_hw_score = points

  return lowest_hw



# Connect to the database.
connection = pymongo.MongoClient("mongodb://localhost")

db = connection.school
students = db.students

# Find students with at least one homework score.
query    = {"scores.type": "homework"}
selector = {"scores": 1}
hw_students = students.find(query, selector)

# Iterate over students and remove each student's lowest score.
for student in hw_students:

  student_id = student["_id"]
  print "Student ", student_id

  lowest_hw = find_lowest_homework(student["scores"])
  if lowest_hw is not None:
    try:
      print "Removing lowest HW: ", lowest_hw
      students.update({"_id": student_id}, {"$pull": {"scores": lowest_hw}})
    except:
      print "Unable to remove lowest HW: ", lowest_hw

