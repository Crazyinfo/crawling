import pymysql

############# 数据库连接部分 #############

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）  
db = pymysql.connect("localhost", "infinitor", "1998328lll", "homework", charset="gbk") #记住要设置编码
# 使用 cursor() 方法创建一个游标对象 cursor  
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询  
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.  
data = cursor.fetchone()
print("连接成功！数据库版本号 : %s " % data)

print("===============数据库查询================")

############# 数据库查询部分 #############

sql = "SELECT * FROM student_work"

try:
	# 执行SQL语句
	cursor.execute(sql)
	# 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		id = row[0] #学号
		name = row[1] #姓名
		sex = row[2] #性别
		age = row[3] #年龄
		department = row[4] #系别
		# 打印结果
		print("学号=%s    姓名=%s    性别=%s    年龄=%s    系别=%s" % \
		      (id, name, sex, age, department))
except:
	print("错误发生：获取数据失败")


# print("===============数据库插入================")
#
# ############# 数据库插入部分 #############
#
# sql = """INSERT INTO student_work(学号, 姓名, 性别, 年龄, 所在系) VALUES(88888882,'插入名','男',88,'管理学院');"""
# try:
#    # 执行sql语句
#    cursor.execute(sql)
#    # 提交到数据库执行
#    db.commit()
# except:
#    # 如果发生错误则回滚
#    db.rollback()
#
# ############# 插入以后再来查一次 #############
#
# sql = "SELECT * FROM student_work"
#
# try:
# 	# 执行SQL语句
# 	cursor.execute(sql)
# 	# 获取所有记录列表
# 	results = cursor.fetchall()
# 	for row in results:
# 		id = row[0] #学号
# 		name = row[1] #姓名
# 		sex = row[2] #性别
# 		age = row[3] #年龄
# 		department = row[4] #系别
# 		# 打印结果
# 		print("学号=%s    姓名=%s    性别=%s    年龄=%s    系别=%s" % \
# 		      (id, name, sex, age, department))
# except:
# 	print("ERROR：获取数据失败")

print("===============数据库更新================")

############# 更新语句  #############
# SQL 更新语句
sql = "UPDATE student_work SET 姓名 = '帅锅' WHERE 学号 = 88888882"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()


############# 更新以后再来查一次 #############

sql = "SELECT * FROM student_work"

try:
	# 执行SQL语句
	cursor.execute(sql)
	# 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		id = row[0] #学号
		name = row[1] #姓名
		sex = row[2] #性别
		age = row[3] #年龄
		department = row[4] #系别
		# 打印结果
		print("学号=%s    姓名=%s    性别=%s    年龄=%s    系别=%s" % \
		      (id, name, sex, age, department))
except:
	print("ERROR：获取数据失败")

print("===============数据库删除================")


############# 删除语句   #############

# SQL 删除语句
sql = "DELETE FROM student_work WHERE 学号  = 88888882"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交修改
    db.commit()
except:
    # 发生错误时回滚
    db.rollback()

############# 删除以后再来查一次 #############

sql = "SELECT * FROM student_work"

try:
	# 执行SQL语句
	cursor.execute(sql)
	# 获取所有记录列表
	results = cursor.fetchall()
	for row in results:
		id = row[0] #学号
		name = row[1] #姓名
		sex = row[2] #性别
		age = row[3] #年龄
		department = row[4] #系别
		# 打印结果
		print("学号=%s    姓名=%s    性别=%s    年龄=%s    系别=%s" % \
		      (id, name, sex, age, department))
except:
	print("ERROR：获取数据失败")

# 关闭数据库连接  
db.close()  
