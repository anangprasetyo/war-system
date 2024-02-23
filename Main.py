import time
import random
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

def check_valid_topik(pilihan=""):
    status = True

    if pilihan!="":
        opsi = db.reference("/pilihan").get()
        if not opsi=='':
            for n in opsi:
                temp = db.reference("/pilihan/" + n).get()
                if temp["judul"] == pilihan:
                    status = False
    
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
        rnd = random.uniform(0, 3)
        time.sleep(rnd)
        if validasi_awal(nim):
            st.info("Pastikan nim sudah sesuai")
            
        elif pilihan == "Tidak ada":
            st.info("Pilih Topik terlebih dahulu")
        
        else:
            if check_valid_pemilih(nim) and check_exist_pemilih(nim):
                if check_valid_topik(pilihan):
                    for t in topik:
                        temp = db.reference("/topik/" + t).get()
                        if temp["judul"] == pilihan:
                            db.reference("/topik/" + t).update({"status": False})
                            pemilih = db.reference("/pemilih/" + "p" + nim).get()
                            db.reference("/pilihan").update({"p" + nim: {"nim": int(nim), "nama": pemilih["nama"], "judul": pilihan}})
        
                    st.info("Selamat anda berhasil memilih topik " + pilihan)
                else:
                    st.info("Topik sudah tidak dapat dipilih")
                time.sleep(1)
                st.rerun()
            else:
                if check_valid_pemilih(nim):
                    st.info("Anda tidak memiliki hak untuk memilih")
                else:
                    st.info("Anda sudah memilih topik")
                time.sleep(1)
                st.rerun()
