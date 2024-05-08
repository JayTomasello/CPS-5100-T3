import pymongo
import dbconfig
from dbconfig import myclient
from dbconfig import mydb
import datetime

#Current test user password: provolone
mycol = mydb["User"]

#Insert Many with Ids Specified
mylist = [
  { "name": "Ric Landarojo", "u_email": "rlandarojo@bean.edu", "password": "chuckchez1", "created": datetime.datetime.utcnow()},
  { "name": "Christoph Hans Engderson", "u_email": "hansengchr@bean.edu", "password": "14md0Cter","created": datetime.datetime.utcnow()},
  { "name": "Spencer Eve", "u_email": "evespenc@bean.edu", "password": "regretdecision","created": datetime.datetime.utcnow()}
]

x = mycol.insert_many(mylist)

# myfavorlist = [
#     {
#         "requester_id": ObjectId("user_id"),
#         "title": "Help with moving",
#         "description": "Need assistance with moving furniture to a new apartment.",
#         "monetary_value": 50,
#         "deadline": datetime.datetime(2024, 3, 10),
#         "category": "Moving",
#         "status": "Created",
#         "comments": [],
#         "pick_up_location": "123 Main St",
#         "drop_off_location": "456 Elm St"
#     },
#     {
#         "requester_id": ObjectId("user_id"),
#         "title": "Tutoring in Math",
#         "description": "Looking for a math tutor to help with calculus homework.",
#         "monetary_value": 30,
#         "deadline": datetime.datetime(2024, 3, 15),
#         "category": "Education",
#         "status": "Created",
#         "comments": [],
#         "pick_up_location": None,
#         "drop_off_location": None
#     }
# ]
