from flask import Flask , render_template , jsonify , request , url_for , redirect , make_response
from pymongo import MongoClient
import random
import os
import json
from datetime import datetime


Key = 'Hello World'
linkdb = 'mongodb+srv://fareladitya1811:root@cluster0.at8lp6a.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(linkdb)
db = client.lampungsolusi


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/image'

@app.errorhandler(404)
def error404(e):
    return render_template('error.html') , 404


@app.route("/")
def home():
    cookie = request.cookies.get('mytoken')
    try:
        token = json.loads(cookie)
        user_info = db.users.find_one({"nik": token["nik"]}, {'_id' :False , 'pw' : False})
        return render_template('index.html' , user_info=user_info)
    except Exception as e:
        print(e)
        return redirect(url_for('login'))


@app.route("/login")
def login():
    response = request.args.get('response')
    
    return render_template("login.html" , response=response)

@app.route("/pushform" , methods=["POST" , "GET"])
def push():
    try :
        nik = request.form['nik']
        password = request.form['password']
        user = db.users.find_one({'nik' : nik})
        if user and password == user['pw']:
            payload = json.dumps({
                'nik' : nik,
                'level' : 'masyarakat'
            })
            make = make_response(redirect(url_for('home')))
            make.set_cookie('mytoken', payload ,max_age=18000 , path='/' ,secure=True)
            return make
        else :
            response = 'Maaf akun tidak ditemukan'
            return redirect(url_for('login', response = response))
    except :
        response = 'Kesalahan dalam memuat halaman'
        return redirect(url_for("login" , response=response))

@app.route('/signup')
def signup():
    error = request.args.get('error')
    return render_template('signup.html' , error=error)

@app.route('/signuping' , methods=["POST"])
def signuping():
    try :
        nik = str(request.form["nik"])
        notlp = str(request.form["notlp"])
        name = request.form["name"]
        username = request.form["username"]
        pw = request.form["password"]
        payload = {
            'nik' : nik,
            'nama' : name,
            'username' : username,
            'pw' : pw,
            'notlp' : notlp,
        }
        try :
            db.users.find_one({'nik': nik})
            error = 'NIK Sudah digunakan...'
            return redirect(url_for('signup' , error=error))
        except :
            db.users.insert_one(payload)
            return redirect(url_for('login'))
    except :
        error = 'kesalahan dalam melakukan pendaftaran...'
        return redirect(url_for('signup' , error=error))

@app.route('/sendcom' , methods=["POST"])
def send():
    token = request.cookies.get("mytoken")
    try:
        cookie = json.loads(token)
        user = db.users.find_one({"nik" : cookie["nik"]})
        text = request.form["text"]
        uniq_p = random.randint(100000, 999999)
        uniq_i = random.randint(100000, 999999)
        time = datetime.now().strftime("%Y-%m-%d")
        try :
            img = request.files["image"]
            file_extension = os.path.splitext(img.filename)[-1]
            image = f'{uniq_i}{file_extension}'
            img.save(os.path.join('static/image', image))
            command = {
                "id_pengaduan" : uniq_p,
                "tgl_pengaduan" : time, 
                "nik" : user["nik"],
                "isi_laporan" : text,
                "foto" : f'/static/image/{image}',
                "status" : "proses"
            }
        except Exception as a:
            command = {
                "id_pengaduan" : uniq_p,
                "tgl_pengaduan" : time, 
                "nik" : user["nik"],
                "isi_laporan" : text,
                "foto" : "",
                "status" : "proses"
            }
            print(a)
            print(command)

        db.msg.insert_one(command)
        return jsonify({
            "result" : "Pengiriman Laporan berhasil"
        })
    except Exception as a:
        print(a)

        return jsonify({
            "result" : "Terjadi kesalahan saat mengirim , Mohon coba sesaat lagi!!"
        })
    
@app.route("/getcom" , methods=["GET"])
def getcom():
    token = request.cookies.get("mytoken")
    try :
        cookie = json.loads(token)
        user = db.users.find_one({"nik" : cookie["nik"]})
        com = db.msg.find({"nik": user["nik"]}, {"_id": False})
        command = list(com)
        return jsonify({
            "data" : command
        })
    except :
        return jsonify({
            "error" : "Laporan tidak di temukan."
        })

@app.route("/cektanggapan/<id>")
def cektanggapan(id):
    token = request.cookies.get("mytoken")
    try :
        cookie = json.loads(token)
        user = db.users.find_one({"nik" : cookie["nik"]})
        laporan = db.msg.find_one({"id_pengaduan" : int(id) , "nik" : user["nik"]})
        tanggapan = db.tanggapan.find_one({"id_pengaduan" : laporan["id_pengaduan"]})
        return render_template("cektanggapan.html", laporan=laporan , tanggapan=tanggapan)
    except:
        return render_template("cektanggapan.html")

@app.route("/profile")
def profile():
    token = request.cookies.get("mytoken")
    try :
        cookie = json.loads(token)
        user = db.users.find_one({"nik" : cookie["nik"]})
        return render_template("profile.html" , user=user)
    except:
        return redirect(url_for('login'))


@app.route("/logout" , methods=["GET" , "POST"])
def logout():
    res = make_response(redirect(url_for("home")))
    res.set_cookie("mytoken" , '', expires=0)
    res.set_cookie("mycookie" , '', expires=0)
    return res

@app.route("/logadmin" , methods=["POST"])
def logadmin():
    try :
        id = request.form["id"]
        pw = request.form["password"]
        account = db.admins.find_one({"id_petugas" : id , "password" : pw})
        payload = json.dumps({
           'id_petugas' : account["id_petugas"],
           'nama_petugas' : account["nama_petugas"],
           'username' : account["username"]
           })
        res = make_response(redirect(url_for("admin")))
        res.set_cookie('mycookie', payload ,max_age=18000 , path='/' , secure=True)
        return res
    except Exception as a:
        print(a)
        response = 'Akun tidak di temukan'
        return redirect(url_for("login" , response=response))

@app.route("/admin")
def admin():
    cookie = request.cookies.get("mycookie")
    try:
        token = json.loads(cookie)
        account = db.admins.find_one({"id_petugas" : token["id_petugas"] , 'nama_petugas' : token["nama_petugas"], 'username' : token["username"]})
        return render_template("admin.html" , account=account)
    except:
        return redirect(url_for("login"))
    
@app.route("/comproses" , methods=["GET"])
def getcomadmin ():
    cookie = request.cookies.get("mycookie")
    try:
        con = request.args.get('con')
        print(con)
        token = json.loads(cookie)
        account = db.admins.find_one({"id_petugas" : token["id_petugas"] , 'nama_petugas' : token["nama_petugas"],'username' : token["username"]})
        if con == 'proses':
            data = list(db.msg.find({"status": "proses"} ,{"_id":False}))
            payload = {
                "result" : "success",
                "data" : data
            }
            return jsonify(payload)
        else:
            data = list(db.msg.find({"status":"selesai"} , {"_id":False}))
            payload = {
                "result" : "success",
                "data" : data
            }
            return jsonify(payload)
    except Exception as a:
        return jsonify({
            "result" : "error",
            "data" : "Tidak di temukan data"
        })

@app.route('/tanggapan/<id>')
def tanggapan(id):
    cookie = request.cookies.get("mycookie")
    try:
        token = json.loads(cookie)
        account = db.admins.find_one({"id_petugas" : token["id_petugas"] , 'nama_petugas' : token["nama_petugas"],'username' : token["username"]})
        laporan = db.msg.find_one({"id_pengaduan" : int(id)}, {"_id" : False})
        if laporan["status"] == "proses":
            print(laporan)
            return render_template("tanggapan.html" , laporan=laporan)
        else :
            tanggapan = db.tanggapan.find_one({"id_pengaduan":laporan["id_pengaduan"]})
            return render_template("tanggapan.html" , laporan=laporan , tanggapan=tanggapan)
    except:
        return render_template("tanggapan.html")

@app.route('/sendtanggapan' , methods=["POST"])
def sendtanggapan():
    cookie = request.cookies.get("mycookie")
    try:
        token = json.loads(cookie)
        account = db.admins.find_one({"id_petugas" : token["id_petugas"] , 'nama_petugas' : token["nama_petugas"],'username' : token["username"]})
        text = request.form["text"]
        id = request.form["id"]
        laporan = db.msg.find_one({"id_pengaduan" : int(id)})
        uniq_t = random.randint(100000, 999999)
        time = datetime.now().strftime("%Y-%m-%d")
        payload = {
            "id_tanggapan" : uniq_t,
            "id_pengaduan" : laporan["id_pengaduan"],
            "tgl_tanggapan" : time,
            "tanggapan" : text,
            "id_petugas" : account["id_petugas"]
        }

        db.msg.update_one({"id_pengaduan" : laporan["id_pengaduan"]} , {"$set" : {"status" : "selesai"}})
        db.tanggapan.insert_one(payload)
        return jsonify({
            "result" : "success"
        })
    except Exception as a:
        print(a)
        return jsonify({
            "result" : "terjadi kesalahan ketika mengirim"
        })
if __name__ == "__main__":
    app.run(debug=True)
