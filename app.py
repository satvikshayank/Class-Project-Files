from flask import Flask,render_template,request,redirect,url_for,session
import mysql.connector
import webbrowser as wb
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="",
                               database="user_login")
cursor = mydb.cursor()

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login',methods=['POST'])
def login():
    username=''
    email = request.form.get('logemail')
    password = request.form.get('logpass')
    cursor.execute("""SELECT * FROM `user` WHERE `username`='{}' and `password`='{}'""".format(email,password))
    users = cursor.fetchall()
    if len(users)>0:
        session['name']=request.form.get('logemail')
        session['user_id']=users[0][0]
        return redirect (url_for("index"))
    else:
        return render_template ("login.html")

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/signup',methods=['POST'])
def Signup():
    name=request.form.get('reguser')
    password=request.form.get('regpass')
    email=request.form.get('regemail')
    cursor.execute("""INSERT INTO `user`(`id`, `name`,`username`, `password`) VALUES (NULL,'{}','{}','{}')""".format(name,email,password))
    mydb.commit()
    return redirect (url_for('home'))

@app.route('/logout')
def pop():
    session.pop('user_id')
    return redirect (url_for('home'))

@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('index.html')

@app.route('/results',methods=['GET'])
def result():
    name = request.args.get("product_name")
    import requests
    from bs4 import BeautifulSoup as bs

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    link_olx = "https://www.olx.in/items/q-"+name+"?isSearchCall=true"
    link_ama = "https://www.amazon.in/s?k="+name+"&ref=nb_sb_noss_2"
    link_flip = "https://www.flipkart.com/search?q="+name+"&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_6_na_na_na&as-pos=1&as-type=HISTORY&suggestionId="+name+"%7CMobiles&requestId=32f2ac2f-0aba-4ec2-aca5-2e4bf7e1356b"
    link_gog = "https://www.google.com/search?tbm=shop&hl=en-GB&psb=1&q="+name

    
    page_olx = requests.get(link_olx, headers=HEADERS)
    page_ama = requests.get(link_ama, headers=HEADERS)
    page_flip = requests.get(link_flip)
    page_gog = requests.get(link_gog, headers=HEADERS)

    soup_olx = bs(page_olx.text, "html.parser")
    name_olx = soup_olx.find_all('span', class_='_2tW1I')
    price_olx = soup_olx.find_all('span', class_='_89yzn')
    img_olx = soup_olx.find_all('img')
    href_olx = soup_olx.find_all('li', class_='EIR5N')

    soup_ama = bs(page_ama.text,"html.parser")
    name_ama = soup_ama.find_all('span',class_='a-size-medium a-color-base a-text-normal')
    price_ama = soup_ama.find_all('span',class_='a-price-whole')
    img_ama = soup_ama.find_all('img',class_='s-image')
    href_ama = soup_ama.find_all('h2',class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2')

    soup_flip = bs(page_flip.text,"html.parser")
    name_flip = soup_flip.find_all('div',class_='_4rR01T')
    price_flip =soup_flip.find_all('div',class_='_30jeq3 _1_WHN1')
    specs_flip = soup_flip.find_all('ul',class_='_1xgFaf')
    img_flip = soup_flip.find_all('img',class_='_396cs4 _3exPp9')
    href_flip = soup_flip.find_all('div',class_='_2kHMtA')

    soup_gog = bs(page_gog.text, "html.parser")
    name_gog = soup_gog.find_all('div', class_='sh-np__product-title translate-content')
    price_gog = soup_gog.find_all('span', class_='T14wmb')
    img_gog = soup_gog.find_all('div',class_='SirUVb sh-img__image')
    href_gog = soup_gog.find_all('div', class_='KZmu8e')
    seller_gog = soup_gog.find_all('span',class_='E5ocAb')


    product_name_olx = []
    product_price_olx = []
    product_img_olx = []
    product_link_olx = []

    product_name_ama =[]
    product_price_ama =[]
    product_img_ama =[]
    product_link_ama =[]

    product_name_flip =[]
    product_price_flip =[]
    product_img_flip =[]
    product_specs_flip = []
    product_link_flip =[]

    product_name_gog = []
    product_price_gog = []
    product_img_gog = []
    product_link_gog = []
    product_seller = []
    
    for i in range(0, len(name_olx)):
        product_name_olx.append(name_olx[i].get_text())
    for i in range(0, len(price_olx)):
        product_price_olx.append(price_olx[i].get_text())
    for i in range(0, len(name_olx)):
        product_img_olx.append(img_olx[i].get("src"))
    for i in range(0, len(name_olx)):
        a_olx = href_olx[i].find('a')
        b_olx = "https://www.olx.in" + str(a_olx.get('href'))
        product_link_olx.append(b_olx)

    for i in range(0,len(name_ama)):
        product_name_ama.append(name_ama[i].get_text())
    for i in range(0,len(price_ama)):
        product_price_ama.append(price_ama[i].get_text())
    for i in range(0,len(img_ama)):
        product_img_ama.append(img_ama[i].get('src'))
    for i in range(0,len(href_ama)):
        a_ama=href_ama[i].find('a')
        b_ama = "https://www.amazon.in"+ str(a_ama.get('href'))
        product_link_ama.append(b_ama)

    for i in range(0,len(name_flip)):
        product_name_flip.append(name_flip[i].get_text())
    for i in range(0,len(price_flip)):
        product_price_flip.append(price_flip[i].get_text())
    for i in range(0,len(specs_flip)):
        product_specs_flip.append(specs_flip[i].get_text())
    for i in range(0,len(img_flip)):
        product_img_flip.append(img_flip[i].get('src'))
    for i in range(0,len(name_flip)):
        a_flip = href_flip[i].find('a')
        b_flip ="http://www.flipkart.in"+ str(a_flip.get('href'))
        product_link_flip.append(b_flip)

    for i in range(0, len(name_gog)):
        product_name_gog.append(name_gog[i].get_text())
    for i in range(0, len(price_gog)):
        product_price_gog.append(price_gog[i].get_text())
    for i in range(0, len(name_gog)):
        a_gog = img_gog[i].find('img')
        b_gog = str(a_gog.get("src"))
        product_img_gog.append(b_gog)
    for i in range(0, len(name_gog)):
        a_gog = href_gog[i].find('a')
        b_gog = str(a_gog.get('href'))
        product_link_gog.append(b_gog)
    for i in range(0, len(name_gog)):
        product_seller.append(seller_gog[i].get_text())
    
    return render_template('search.html',product_name_olx=product_name_olx,product_price_olx=product_price_olx,product_img_olx=product_img_olx,product_link_olx=product_link_olx,
                           product_name_ama=product_name_ama,product_price_ama=product_price_ama,product_img_ama=product_img_ama,product_link_ama=product_link_ama,
                           product_name_flip=product_name_flip,product_price_flip=product_price_flip,product_img_flip=product_img_flip,product_link_flip=product_link_flip,product_specs_flip=product_specs_flip,
                           product_name_gog=product_name_gog,product_price_gog=product_price_gog,product_img_gog=product_img_gog,product_link_gog=product_link_gog,
                           )

@app.route('/category-m')
def cat_m():
    return render_template('cate-m.html')

@app.route('/category-h')
def cat_h():
    return render_template('cate-h.html')

@app.route('/category-sc')
def cat_sc():
    return render_template('cate-sc.html')

@app.route('/category-sk')
def cat_sk():
    return render_template('cate-sk.html')

@app.route('/contact',methods=['POST'])
def contact():
    name=request.form.get('conname')
    email=session['name']
    subject=request.form.get('consubject')
    msg=request.form.get('conmsg')
    cursor.execute("""INSERT INTO `contact`(`name`,`email`,`subject`,`message`)VALUES('{}','{}','{}','{}')""".format(name,email,subject,msg))
    mydb.commit()
    return redirect (url_for('index'))



if __name__ == '__main__':
    app.run()
