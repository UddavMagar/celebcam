from django.http import HttpResponse,JsonResponse
import datetime
import pymongo
from pymongo import MongoClient
def index(request):
    client = MongoClient('localhost', 27017)
    print(client)
    db=client.pramishdb
    print("\n\n\n\ndatabase\n\n\n",db)
    
    post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()
        }
    objpramish = db.objpramish
    print("********\n\n\n\n",objpramish,"********\n\n\n\n")
    post_id = objpramish.insert_one(post)
    print(post_id)
    return JsonResponse({'name':'pramish'})