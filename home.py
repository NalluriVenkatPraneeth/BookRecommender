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
def loginscreen():
    return render_template("login.html")


@app.route('/home/<pageno>',methods=["POST","GET"])
def home(pageno=1):
    dat = pd.read_csv('books_clean.csv')[['img_l','book_title']]
    #dat = dat[dat['year_of_publication']]
    images = dat[(int(pageno)-1)*12:int(pageno)*12]['img_l'].values
    titles = dat[(int(pageno)-1)*12:int(pageno)*12]['book_title'].values
    alltitles = np.array(dat['book_title'].values)
    for i in range(12):
        #print(images[i])
        urllib.request.urlretrieve(
            images[i],
            "static\\"+str(i)+'.jpg')
        img = Image.open('static\\'+str(i)+'.jpg')
        if img.size==(1,1):
            images[i]=""
    print(alltitles)
    users = pd.read_csv('BX-Users.csv', sep=';', encoding='latin-1',low_memory=False)
    #print(users)
    #print(len(dat))
    #print(pageno)
    lenn = len(images)
    titlelen = len(alltitles)
    print(titlelen)
    return render_template("review1.html",images=images,titles=titles,lenn=lenn,titlelen=titlelen,alltitles=alltitles,pageno=pageno)

@app.route('/search/')
@app.route('/search/<pageno>/<texttosearch>',methods=["POST","GET"])
def search(texttosearch,pageno):
    ff=""
    if int(pageno)==1:
        print(pageno)
        print(texttosearch)
        texttosearch = request.form['search']
        print(texttosearch)
    dat = pd.read_csv('books_clean.csv')[['img_l','book_title']]
    dat['book_title'] = dat['book_title'].str.lower()
    dat = dat[dat['book_title'].str.startswith(texttosearch)]
    images = dat[(int(pageno)-1)*12:int(pageno)*12]['img_l'].values
    titles = dat[(int(pageno)-1)*12:int(pageno)*12]['book_title'].values
    alltitles = np.array(dat['book_title'].values)
    if len(dat)>12:
        x = 12
    else:
        x = len(dat)
    for i in range(x):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images[i],
                "static\\"+str(i)+'.jpg')
            img = Image.open('static\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images[i]=""
        except:
            print("Hello")
            ff = "No results found"
    print(alltitles)
    users = pd.read_csv('BX-Users.csv', sep=';', encoding='latin-1',low_memory=False)
    #print(users)
    #print(len(dat))
    #print(pageno)
    lenn = len(images)
    titlelen = len(alltitles)
    print(titlelen)
    return render_template("search.html",ff=ff,texttosearch=texttosearch,images=images,titles=titles,lenn=lenn,titlelen=titlelen,alltitles=alltitles,pageno=pageno)


@app.route('/login',methods=['GET','POST'])
def login():
    ratings = pd.read_csv('cleanusers.csv')
    ratings = ratings[ratings['user_id']==11676]
    uname = request.form['uname']
    psw = request.form['psw']
    #function call to get books for both content,collab
    contentbooks = []
    collab = []
    collabpluscont = ['0971880107', '0316666343', '0385504209', '0060928336', '0312195516', '0142001740', '0679781587', '067976402X', '0671027360', '044023722X']
    #f
    i_cols = ['isbn', 'book_title' ,'book_author','year_of_publication', 'publisher', 'img_s', 'img_m', 'img_l']
    dat = pd.read_csv('BX_Books.csv', sep=';', names=i_cols, encoding='latin-1',low_memory=False)[['img_l','book_title','isbn']]
    recom = pd.DataFrame(columns=dat.columns)
    for i in range(len(dat)):
        if dat['isbn'][i] in collabpluscont:
            recom = recom.append({'img_l':dat['img_l'][i],'book_title':dat['book_title'][i],'isbn':dat['isbn'][i]},ignore_index=True)

    dat = recom
    images = dat['img_l'].values
    titles = dat['book_title'].values
    alltitles = np.array(dat['book_title'].values)
    for i in range(len(dat)):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images[i],
                "static\\"+str(i)+'.jpg')
            img = Image.open('static\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images[i]=""
        except:
            print("Hello")
    lenn = len(images)
    titlelen = len(alltitles)
    print(titlelen)
    return render_template("recommend.html",images=images,titles=titles,lenn=lenn,titlelen=titlelen,alltitles=alltitles)

@app.route('/single/<title>')
def single(title):
    ratings = pd.read_csv('cleanusers.csv')
    ratings = ratings[ratings['user_id']==11676]
    #function call to get books for both content,collab
    contentbooks = []
    collab = []
    collabpluscont = ['0971880107', '0316666343', '0385504209', '0060928336', '0312195516', '0142001740', '0679781587',  '0671027360', '044023722X']
    #f
    i_cols = ['isbn', 'book_title' ,'book_author','year_of_publication', 'publisher', 'img_s', 'img_m', 'img_l']
    dat = pd.read_csv('BX_Books.csv', sep=';', names=i_cols, encoding='latin-1',low_memory=False)
    recom = pd.DataFrame(columns=dat.columns)
    for i in range(len(dat)):
        if dat['isbn'][i] in collabpluscont:
            recom = recom.append({'img_l':dat['img_l'][i],'book_title':dat['book_title'][i],'isbn':dat['isbn'][i]},ignore_index=True)

    dat = recom
    images1 = dat['img_l'].values
    titles1 = dat['book_title'].values
    alltitles1 = np.array(dat['book_title'].values)
    for i in range(len(dat)):
        #print(images[i])
        try:
            urllib.request.urlretrieve(
                images1[i],
                "static\\"+str(i)+'.jpg')
            img = Image.open('static\\'+str(i)+'.jpg')
            if img.size==(1,1):
                images1[i]=""
        except:
            print("Hello")
    lenn1 = len(images1)
    titlelen1 = len(alltitles1)
    print(titlelen1)
    return render_template("single.html",title=title,images=images1,titles=titles1,lenn=lenn1,titlelen=titlelen1,alltitles=alltitles1)

if __name__=='__main__':
    app.run(debug=True)