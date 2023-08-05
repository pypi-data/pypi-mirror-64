from tkinter import ttk,Tk,Label,Entry
from shaonutil.strings import generateCryptographicallySecureRandomString
import tkinter as tk
import mysql.connector as mysql


class MySQL:
	def __init__(self,config,log=False):
		self.log = log
		self.config = config

	def reopen_connection(self):
		print("MySQL > Explicitly opening connection ...")
		self.make_cursor()

	def close_connection(self):
		print("MySQL > Explicitly closing connection ...")
		self._cursor.close()
		self.mySQLConnection.close()

	@property
	def config(self):
		return self._config
		
	@config.setter
	def config(self, new_value):
		self._config = new_value
		self.filter_config()
		self.make_cursor()
	
	def filter_config(self):
		mustList = ['host','user','password']
		for key in self._config:
			if not key in mustList:
				ValueError(key,"should have in passed configuration")
				break

	def make_cursor(self):
		try:
			# Connection parameters and access credentials
			if 'database' in self._config:
				mySQLConnection = mysql.connect(
					host = self._config['host'],
					user = self._config['user'],
					passwd = self._config['password'],
					database = self._config['database']
				)
			else:
				mySQLConnection = mysql.connect(
					host = self._config['host'],
					user = self._config['user'],
					passwd = self._config['password']
				)
			self.mySQLConnection = mySQLConnection

		except mysql.errors.OperationalError:
			print("Error")
			# shaonutil.process.remove_aria_log('C:\\xampp\\mysql\\data')

		self._cursor = mySQLConnection.cursor()

	def is_mysql_user_exist(self,mysql_username):
		mySQLCursor = self._cursor
		mySqlListUsers = "select host, user from mysql.user;"
		mySQLCursor.execute(mySqlListUsers)
		userList = mySQLCursor.fetchall()
		foundUser = [user_ for host_,user_ in userList if user_ == mysql_username]
		if len(foundUser) == 0:
			return False
		else:
			return True

	def listMySQLUsers(self):
		"""list all mysql users"""
		mySQLCursor = self._cursor
		mySqlListUsers = "select host, user from mysql.user;"
		mySQLCursor.execute(mySqlListUsers)
		userList = mySQLCursor.fetchall()
		print("MySQL > List of users:")
		for user in userList:
		    host_,user_ = user
		    print("   ","host =",host_+",","user =",user_)


	def createMySQLUser(self, host, userName, password,
	               querynum=0, 
	               updatenum=0, 
	               connection_num=0):
		cursor = self._cursor
		try:
			print("MySQL > Creating user",userName)
			sqlCreateUser = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';"%(userName,host,password)
			cursor.execute(sqlCreateUser)
		except Exception as Ex:
			print("Error creating MySQL User: %s"%(Ex));

	def grantMySQLUserAllPrivileges(self, host, userName,
	               querynum=0, 
	               updatenum=0, 
	               connection_num=0):
		cursor = self._cursor
		try:
			print("MySQL > Granting all PRIVILEGES to user",userName)
			sqlGrantPrivilage = "GRANT ALL PRIVILEGES ON * . * TO '%s'@'%s';"%(userName,host)
			cursor.execute(sqlGrantPrivilage)
			cursor.execute("FLUSH PRIVILEGES;")

		except Exception as Ex:
			print("Error creating MySQL User: %s"%(Ex));

	def is_db_exist(self,dbname):
		cursor = self._cursor

		cursor.execute("SHOW DATABASES")
		databases = cursor.fetchall()
		databases = [x[0] for x in databases]
		if dbname not in databases:
			return False
		else:
			return True

	def create_db(self,dbname):
		cursor = self._cursor
		print("MySQL > Creating database "+dbname+" ...")
		cursor.execute("CREATE DATABASE "+dbname)

	def is_table_exist(self,tbname):
		cursor = self._cursor
		cursor.execute('SHOW TABLES')
		tables = cursor.fetchall()
		tables = [ x[0] for x in tables ]
		if tbname in tables:
			return True
		else:
			return False

	def create_table(self,tbname,column_info):
		cursor = self._cursor
		print("MySQL > Creating table "+tbname+" ...")
		cursor.execute("CREATE TABLE "+tbname+" (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,"+''.join([' '+info+' '+column_info[info]+',' for info in column_info])[:-1]+")")

	def get_columns(self,tbname):
		cursor = self._cursor
		cursor.execute("SHOW COLUMNS FROM "+tbname)
		columns = cursor.fetchall()
		return columns
		# [('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment'), ('book_sid', 'varchar(255)', 'YES', '', None, ''), ('book_name', 'varchar(255)', 'YES', '', None, ''), ('book_writer', 'varchar(255)', 'YES', '', None, ''), ('book_publisher', 'varchar(255)', 'YES', '', None, '')]

	def get_columns_names(self,tbname):
		columns = self.get_columns(tbname)
		return [column_name for column_name, *_ in columns]

	def get_unique_id_from_field(self,key_length,field_name):
		table = self._config['table']

		cursor = self._cursor

		sid = generateCryptographicallySecureRandomString(key_length)
		
		while True:
			query = "SELECT * FROM "+table+" WHERE `"+field_name+"` = '"+sid+"'"
			print(query)

			## getting records from the table
			cursor.execute(query)

			## fetching all records from the 'cursor' object
			records = cursor.fetchall()

			## Showing the data
			for record in records:
			    print(record)


			if(len(records)>1):
				print("matched with previously stored sid")
				sid = generateCryptographicallySecureRandomString(key_length)
			else:
				print("Got unique sid")
				break
				
		return sid

	def insert_data(self,value_tupple):
		cursor = self._cursor
		dbname = self._config['database']
		tbname = self._config['table']
		column_info = self.get_columns_names(tbname)[1:]
		
		# candidate_name, candidate_age, candidate_distance, candidate_living_place, candidate_university_or_instituition, candidate_image_webp_url, candidate_unique_image_name
		#cursor.execute("DESC "+tbname)
		
		query = "INSERT INTO "+tbname+ ' (' + ''.join([key+', ' for key in column_info])[:-2] + ') VALUES ('+ ''.join(['%s, ' for key in column_info])[:-2]  +')'
		
		## storing values in a variable
		values = [
		    value_tupple
		]

		## executing the query with values
		cursor.executemany(query, values)

		## to make final output we have to run the 'commit()' method of the database object
		self.mySQLConnection.commit()

		print(cursor.rowcount, "record inserted")

def create_configuration(option='cli'):
	if option == 'cli':
		print('Getting your configurations to save it.\n')
		print('\nDatabase configurations -')
		dbhost = input('Give your db host : ')
		dbuser = input('Give your db user : ')
		dbpassword = input('Give your db password : ')
		dbname = input('Give your db name : ')
		dbtable = input('Give your db table : ')

		mysql_bin_folder = input('Give your path of mysql bin folder : ')

		f = open("private/config.ini", "w+")
		f.writelines(["; config file\n", "[db_authentication]\n", "host = "+dbhost+"\n", "user = "+dbuser+"\n", "password = "+dbpassword+"\n", "database = "+dbname+"\n", "table = "+dbtable+"\n","[MYSQL]\n","mysql_bin_folder = "+mysql_bin_folder+"\n","[DB_INITIALIZE]\n","host = localhost\n","usr = root\n","passwd = \n"])
		f.close()
	elif option == 'gui':
		window = Tk()
		window.title("Welcome to DB Config")
		window.geometry('400x400')
		window.configure(background = "grey");

		# Label fb_authentication
		FB_LABEL = Label(window ,text = "MYSQL Config").grid(row = 0,column = 0,columnspan=2)
		a = Label(window ,text = "MYSQL bin folder").grid(row = 1,column = 0)
		
		DB_LABEL = Label(window ,text = "Database Authentication").grid(row = 3,column = 0,columnspan=2)
		c = Label(window ,text = "Host").grid(row = 4,column = 0)
		d = Label(window ,text = "User").grid(row = 5,column = 0)
		d = Label(window ,text = "Password").grid(row = 6,column = 0)
		d = Label(window ,text = "Database").grid(row = 7,column = 0)
		d = Label(window ,text = "Table").grid(row = 8,column = 0)

		mysqlbinfolder_ = tk.StringVar(window)
		fbpassword_ = tk.StringVar(window)
		dbhost_ = tk.StringVar(window)
		dbuser_ = tk.StringVar(window)
		dbpassword_ = tk.StringVar(window)
		dbname_ = tk.StringVar(window)
		dbtable_ = tk.StringVar(window)

		Entry(window,textvariable=mysqlbinfolder_).grid(row = 1,column = 1)
		
		Entry(window,textvariable=dbhost_).grid(row = 4,column = 1)
		Entry(window,textvariable=dbuser_).grid(row = 5,column = 1)
		Entry(window,show="*",textvariable=dbpassword_).grid(row = 6,column = 1)
		Entry(window,textvariable=dbname_).grid(row = 7,column = 1)
		Entry(window,textvariable=dbtable_).grid(row = 8,column = 1)

		def clicked():
			mysql_bin_folder = mysqlbinfolder_.get()
			
			dbhost = dbhost_.get()
			dbuser = dbuser_.get()
			dbpassword = dbpassword_.get()
			dbname = dbname_.get()
			dbtable = dbtable_.get()

			f = open("private/config.ini", "w+")
			f.writelines(["; config file\n", "[db_authentication]\n", "host = "+dbhost+"\n", "user = "+dbuser+"\n", "password = "+dbpassword+"\n", "database = "+dbname+"\n", "table = "+dbtable+"\n","[MYSQL]\n","mysql_bin_folder = "+mysql_bin_folder+"\n","[DB_INITIALIZE]\n","host = localhost\n","usr = root\n","passwd = \n"])
			f.close()
			window.destroy()



		btn = ttk.Button(window ,text="Submit",command=clicked).grid(row=9,column=0)
		window.mainloop()