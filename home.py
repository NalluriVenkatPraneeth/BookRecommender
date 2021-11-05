#Importing Required Libraries
from flask import Flask,render_template,request
import numpy as np
import pickle
from numpy.lib.type_check import imag
import pandas as pd
import urllib.request
from PIL import Image

#Initializing
app = Flask(__name__)

#Home page for the Application
@app.route('/')
@app.route('/home/')
@app.route('/home/<pageno>')
def home(pageno=1):
    dat = pd.read_csv('books_clean.csv')[['img_l','book_title']]
    #dat = dat[dat['year_of_publication']]
    images = dat[(int(pageno)-1)*12:int(pageno)*12]['img_l'].values
    titles = dat[(int(pageno)-1)*12:int(pageno)*12]['book_title'].values
    alltitles = dat['book_title'].values
    for i in range(12):
        #print(images[i])
        urllib.request.urlretrieve(
            images[i],
            "pic.png")
        img = Image.open("pic.png")
        if img.size==(1,1):
            images[i]=""

    users = pd.read_csv('BX-Users.csv', sep=';', encoding='latin-1',low_memory=False)
    #print(users)
    #print(len(dat))
    #print(pageno)
    lenn = len(images)
    return render_template("review1.html",images=images,titles=titles,lenn=lenn,alltitles=alltitles,pageno=pageno)

#Url for Regression analysis
@app.route('/login')
def login():
    return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)