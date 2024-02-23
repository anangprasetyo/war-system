import time
import streamlit as st
import firebase_admin
from firebase_admin import db, credentials

if not firebase_admin._apps:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"databaseURL": "https://war-systems-default-rtdb.firebaseio.com/"})

def check_exist_pemilih(val=""):
    status = True
    
    pilihan = db.reference("/pilihan").get()
    if not pilihan=='':
        for p in pilihan:
            temp = db.reference("/pilihan/" + p).get()
            if temp["nim"] == int(val):
                status = False

    return status

def check_valid_pemilih(val=""):
    status = False

    pemilih = db.reference("/pemilih").get()
    for p in pemilih:
        temp = db.reference("/pemilih/" + p).get()
        if temp["nim"] == int(val):
            status = True

    return status

def validasi_awal(nim=""):
    status = False

    if nim=="":
        status = True
    
    return status

with st.form(key="myform", clear_on_submit=True):
    title = db.reference("/title").get()
    topik = db.reference("/topik").get()
    st.title(title)
    listTopik = []
    listTopik.append("Tidak ada")

    for t in topik:
        temp = db.reference("/topik/" + t).get()
        if temp["status"] == True:
            listTopik.append(temp["judul"])

    nim = st.text_input("NIM")
    pilihan = st.radio("Pilih Topik Riset", listTopik)
    submit_btn = st.form_submit_button('Submit', type="primary")

    if submit_btn:
        time.sleep(1)
        if validasi_awal(nim):
            st.info("Pastikan nim sudah sesuai")
            
        elif pilihan == "Tidak ada":
            st.info("Pilih Topik terlebih dahulu")
        
        else:
            if check_valid_pemilih(nim) and check_exist_pemilih(nim):
                for t in topik:
                    temp = db.reference("/topik/" + t).get()
                    if temp["judul"] == pilihan:
                        db.reference("/topik/" + t).update({"status": False})
                        pemilih = db.reference("/pemilih/" + "p" + nim).get()
                        db.reference("/pilihan").update({"p" + nim: {"nim": int(nim), "nama": pemilih["nama"], "judul": pilihan}})
    
                st.info("Selamat anda berhasil memilih topik " + pilihan)
                time.sleep(1)
                st.rerun()
            else:
                if check_valid_pemilih(nim):
                    st.info("Anda tidak memiliki hak untuk memilih")
                else:
                    st.info("Anda sudah memilih topik")
                time.sleep(1)
                st.rerun()
