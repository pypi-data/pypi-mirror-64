import os
from pymongo import MongoClient


def say_hello(name):
    myclient = MongoClient("localhost", 27017)
    mydb = myclient["mydb"]
    mycol = mydb["mycollection"]
    myid = mycol.insert_one({"a": 1}).inserted_id
    return "The inserted id is {0}".format(myid)
