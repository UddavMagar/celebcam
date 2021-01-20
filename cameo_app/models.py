from pymongo import MongoClient
import datetime
import gridfs

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


def celebrity_model(celebrityname):
	data = db.celebrity_detail.find_one({'celibrityname':celebrityname})
	if data:
		return data['lastname'], data['feature'], data['description'], data['videorate'], data['chatrate']


def request_model(loginuser, celebrityname, servicetype, message):
	db.request_service.insert_one({'loginuser':loginuser,'celebrityname':celebrityname,'servicetype':servicetype,'message':message})
	

def celebrity_request_model(celebrityname,servicetype):
	data = db.request_service.find({'celebrityname':celebrityname,'servicetype':servicetype})
	if data:
		return data


def video_upload(video, requestuser, celebrityname):
	filename = "/home/uddav/Videos/"+video
	datafile = open(filename, "rb")
	thedata = datafile.read()
	fs = gridfs.GridFS(db)
	fs.put(thedata, filename=video)
	db.request_service.remove({'loginuser':requestuser,'servicetype':'video'})


def video_download(loginuser):
	fs = gridfs.GridFS(db)
	dataname = db.video_detail.find_one({'requestuser':loginuser})
	name = dataname['videoname']
	data = db.fs.files.find_one({'filename':name})
	my_id= data['_id']
	outputdata =fs.get(my_id).read()
	outfilename = "/home/uddav/Downloads"+name
	output= open(outfilename,"wb")
	output.write(outputdata)
	output.close()
	db['fs.chunks'].remove({'files_id':my_id})
	db['fs.files'].remove({'_id':my_id})
	db.video_detail.remove({'videoname':name})
	
	


def video_detail(video, requestuser, celebrityname):
	db.video_detail.insert_one({'requestuser':requestuser,'celebrityname':celebrityname,'videoname':video})


def notification_count(loginuser):
	data = db.video_detail.find({'requestuser':loginuser})
	data1 = db.chat_detail.find({'requestuser':loginuser})
	count =0
	for i in data:
		count+=1
	for i in data1:
		count+=1
	return count


def user_video_info(loginuser):
	data = db.video_detail.find({'requestuser':loginuser})
	return data


def user_chat_info(loginuser):
	data = db.chat_detail.find({'requestuser':loginuser})
	return data


def chat_time(datestring,requestuser,celebrityname):
	datetime_object = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M')
	hours_added = datetime.timedelta(hours = 1)
	future_date_and_time = datetime_object + hours_added
	data = db.chat_detail.find({'celebrityname':celebrityname})
	for i in data:
		if (i['nowdatetime']<=datetime_object<=i['futuredatetime']):
			return 'error'
		elif (i['nowdatetime']<=future_date_and_time<=i['futuredatetime']):
			return 'error'
	db.chat_detail.insert_one({'requestuser':requestuser,'celebrityname':celebrityname,
	'nowdatetime':datetime_object,'futuredatetime':future_date_and_time})
	db.request_service.remove({'loginuser':requestuser,'celebrityname':celebrityname,'servicetype':'Chat'})
	
		
def comment_model(celebrityname,loginuser,message):
	db.comment.insert_one({'celebrityname':celebrityname,'loginuser':loginuser,'message':message})

def comments(celebrityname):
	data = db.comment.find({'celebrityname':celebrityname})
	return data


def chat_start(loginuser):
	data = db.chat_detail.find_one({'requestuser':loginuser})
	if data == None:
		return False	
	now = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=45)
	if data['nowdatetime']<=now<=data['futuredatetime']:
		return True
	else:
		return False


def celebrity_chat_start(celebrityname):
	data = db.chat_detail.find_one({'celebrityname':celebrityname})	
	if data == None:
		return False	
	now = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=45)
	if data['nowdatetime']<=now<=data['futuredatetime']:
		return True
	else:
		return False


def other_user(loginuser):
	data = db.chat_detail.find_one({'requestuser':loginuser})
	return data['celebrityname']


def celebrity_other_user(celebrityname):
	data = db.chat_detail.find_one({'celebrityname':celebrityname})
	return data['requestuser']



def chat_end(loginuser):
	data = db.chat_detail.find_one({'requestuser':loginuser})
	if data == None:
		return None
	now = datetime.datetime.now()+datetime.timedelta(hours=5,minutes=45)
	futuretime = data['futuredatetime']+datetime.timedelta(hours=1)
	if now>futuretime:
		db.chat_detail.remove({'requestuser':loginuser})
		
	