from pymongo import MongoClient
import datetime

def mongo_conn():
    try:
        print ("mongo")
        conn = MongoClient(host='127.0.0.1', port=27017)
        print("MongoDB Connected", conn)
        return conn.chat_application
    except Exception as e:
        print ("Error in mongo connection: ", e)


db = mongo_conn()

def register_model(name, password, phone, email):
	db.user_master.insert({'name':name,'email':email,'password':password,'phone':phone,'user_type':"fans"})
	

def login_model(name, pwd):
	data = db.user_master.find_one({'name':name, 'password':pwd})
	if data:
		return data['user_type']


def is_active(uname,utype):
	db.user_master.update({'name':uname,'user_type':utype},{'$set':{'active':1}})

def is_inactive(uname,utype):
	db.user_master.update({'name':uname,'user_type':utype},{'$set':{'active':0}})


def is_online(current_user):
	online_users = []
	db_data = db.user_master.find({'active':1})
	print("****active*****",db_data)
	for data in db_data :
		if data.get('name') != current_user:
			online_users.append(data.get('name'))
	return online_users



def chat_db(from_m,to,msg):
    now = datetime.datetime.now()
    db.chat_db.insert({"msg_from":from_m, "msg_to" : to, "text_msg": msg , "timestamp" : now})



def get_all_msg_db(frm,to):
	msg = []
	db_data =  db.chat_db.find(
		{
			'msg_from': {'$in':[frm,to]},
			'msg_to' : {'$in': [frm,to]}
		}
	)
	for data in db_data:
		msg.append(data)
    # cursor = db.cursor()
    # # stmt = """ Select message, msg_from, msg_to from chat_db where msg_from = '%s' or msg_to = '%s' """%(frm,to)
    # stmt = """ SELECT * FROM `chat_db` WHERE msg_from IN('%s','%s') and msg_to IN('%s','%s') """%(frm,to,frm,to)
    # cursor.execute(stmt);
    # c = cursor.fetchall()
    # # print "messages   ", c
    # return c
	return msg
