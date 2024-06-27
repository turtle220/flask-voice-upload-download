#Indentation is 4 spaces.
#Available routes : /download/filehash  /upload  /server-usage /disk-usage
import hashlib
import os
import sqlite3
from datetime import date
from flask import Flask ,render_template ,request, redirect, url_for ,g ,jsonify ,send_from_directory , send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'download'

DATABASE='./database/files.db'

# Ensure the upload and download folders exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 Please note this is max upload limit by flask which is 16mb now

#Database Connect function as given in flask docs
#Table schema CREATE TABLE files (id INTEGER PRIMARY KEY AUTOINCREMENT,filename VARCHAR,size VARCHAR,hash VARCHAR,date VARCHAR,counter VARCHAR);
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db

#Database query function to return raw data from database
def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv
		
#index page get request
@app.route('/download_output', methods=['GET'])
def download_output():
    try:
        text_content = request.args.get('text_content')
        upload_result = request.args.get('upload_result')
        
        print(text_content)
        print(upload_result)
        
        # Path to the requirements.txt file using configured download_path
        download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), app.config['DOWNLOAD_FOLDER'])
        file_path = os.path.join(download_path, "test.txt")
        
        print("file_path:", file_path)
        return send_file(file_path, as_attachment=True)

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error: File download failed", 500

@app.route("/")
def index():
	return render_template('upload.html')


#Upload get and post method to save files into directory
@app.route("/upload",methods=['GET','POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(directory)
        size = os.path.getsize(directory)
        with open(directory, 'rb') as f:
            file_content = f.read()
            filehash = hashlib.sha1(file_content).hexdigest()
        inserted_id = db_insert(filename, size, filehash)
        if inserted_id:
            os.rename(directory, os.path.join(app.config['UPLOAD_FOLDER'], filehash))
            return jsonify({"filehash": filehash, "id": inserted_id})  # Return JSON response with file hash and ID
        else:
            return 'Upload Failed', 500


@app.route("/download/<filehash>",methods=['GET'])
def download(filehash):
		#filehash is sha1 hash stored in database o f file.Increase download counter
		data=query_db('select * from files where hash=?',[filehash])
		counter=int(data[0][5])+1
		print('------upload download------')
		try:
			get_db().execute("update files SET counter = ? WHERE hash=?", [counter,filehash])
			get_db().commit()
			#return send_from_directory(app.config['UPLOAD_FOLDER'], data[0][3])
			return send_file(os.path.join(app.config['UPLOAD_FOLDER'], data[0][3]),attachment_filename=data[0][1],as_attachment=True)
		except:
			return 'File not Found'

@app.route("/server-usage",methods=['GET'])
def server_usage():
	data=query_db('select * from files')
	bandwidth=0
	for i in data:
		bandwidth+=int(i[5])*int(i[2]) #Multiplying counter with size of file to get bandwidth amount
	return jsonify(bandwidthusage=str(bandwidth/1024.0)+" KB")


@app.route("/disk-usage",methods=['GET'])
def disk_usage():
	data=query_db('select * from files')
	diskspace=0
	for i in data:
		diskspace+=int(i[2])
	return jsonify(diskusage=str(diskspace/1024.0)+" KB")


#Its a simple function just return number of files link should be /db for application
@app.route("/db")
def db_table():
	data=query_db('select * from files')
	return jsonify(values=data)
	#for user in data:
    #	return user['filename'], user['size']

def db_insert(filename,size,filehash):
		filename=str(filename)
		size=int(size)
		filedate=str(date.today())
		file_exist=query_db('select * from files where hash=?',[filehash])
		if not file_exist:
			get_db().execute("insert into files (filename,size,hash,date,counter) values (?,?,?,?,?)", [filename,size,filehash,filedate,0])
			get_db().commit()
		else:
			cursor = get_db().cursor()
			cursor.execute("INSERT INTO files (filename, size, hash, date, counter) VALUES (?, ?, ?, ?, ?)",
						(filename, size, filehash, filedate, 0))
			get_db().commit()
			
			# Retrieve the ID of the inserted record
			row_id = cursor.lastrowid
			
			# Close cursor after use
			cursor.close()
			
			return row_id


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
