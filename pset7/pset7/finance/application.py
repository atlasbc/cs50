from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    
    real_rows = []
    symbols = []
    total_value = 0
    
    # extract which company's stock user bought
    rows = db.execute("SELECT * FROM transactions WHERE id = :id GROUP BY symbol", 
                    id=session["user_id"])
    for row in rows:
        if row["symbol"] not in symbols:
            symbols.append(row["symbol"])
    
    # extract one specific stock's data
    for symbol in symbols:
        
        #initialize a dictionary for one specific stock
        stock_index = {'symbol': None, 'name': None, 'quantity': None, 'price': None, 'total': None}  
        
        #search database and record shares
        shares_raw = db.execute("SELECT sum(quantity) FROM transactions WHERE id = :id and symbol = :symbol",
                            id=session["user_id"], symbol=symbol)
        shares = shares_raw[0]["sum(quantity)"]                    
        
        # skip if user has 0 shares
        if shares == 0:
            continue
        
        # one stock's data  
        stock = lookup(symbol)
        stock_index['symbol'] = stock['symbol'] 
        stock_index['name'] = stock['name']
        stock_index['price'] = stock['price']
        stock_index['quantity'] = shares
        stock_index['total'] = stock['price']*shares
        
        # calculate total value of stocks
        total_value = total_value + stock_index['total']
        
        # record data as one row
        real_rows.append(stock_index)
    
    # extract cash amount from database    
    user_row = db.execute("SELECT * FROM users WHERE id = :id", 
                        id=session["user_id"])        
    user_cash = float (user_row[0]['cash'])    
        
    return render_template("index.html", stocks=real_rows, 
                            cash=user_cash, total=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # find company's stock and take share number
        stock = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        
        # if stock doesnt exist
        if not stock:
            return apology("Invalid Symbol")
        
        #shares are not entered
        if not shares:
            return apology("missing shares")
        
        #convert shares str to int and check validity     
        share_number = int (shares)
        if share_number <= 0:
            return apology("you must give me valid share numbers")
        
        # stock variables
        stock_price = stock['price']
        stock_name = stock['name']
        stock_symbol = stock['symbol']
        
        # total share cost
        share_price = stock_price*share_number
        
        # query database for username
        user_row = db.execute("SELECT * FROM users WHERE id = :id", 
                            id=session["user_id"])        
        user_cash = float (user_row[0]['cash'])
        
        if share_price > user_cash:
            return apology("can not afford")
            
        # flash message
        flash("Bought!")    
            
        # update cash
        user_cash = user_cash - share_price
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", 
                    cash=user_cash, id=session["user_id"]) 
        
        # record transaction
        db.execute("INSERT INTO transactions (id, symbol, price, quantity, total) VALUES(:id, :symbol, :price, :quantity, :total)",
                    id=session["user_id"], symbol=stock_symbol, price=stock_price, quantity=share_number, total=share_price)
        
        return redirect(url_for("index"))
        
    # else if user reached route via GET (as by clicking a link or via redirect)    
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    
    rows = db.execute("SELECT * FROM transactions WHERE id = :id", 
                    id=session["user_id"])
    if not rows:
        return apology("you do not have a history kid")
        
    return render_template("history.html", stocks=rows)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", 
                        username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # search for company data
        quote = lookup(request.form.get("symbol"))
        
        # if company's symbol is wrong
        if not quote:
            return apology("symbol does not exist")
            
        return render_template("quoted.html", name=quote['name'], symbol=quote['symbol'], price=quote['price'])
        
    # else if user reached route via GET (as by clicking a link or via redirect)    
    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        
        # ensure password check was submitted
        elif not request.form.get("password2"):
            return apology("must provide password check")
        
        # ensure user didn't do typo    
        elif not request.form.get("password") == request.form.get("password2"):
            return apology("passwords do not match", "you did typo then")
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # check whether username exists
        if len(rows) == 1:
            return apology("this username already exist")        
        
        # hash the password
        password = request.form.get("password")
        hash = pwd_context.hash(password)
        
        # 
        result = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"), hash=hash)
        # database failed           
        if not result:
            return apology("can not register")
        
        # flash message
        flash("You Registered! You can login now.") 
            
        # redirect user to login page, because she/he succeeded
        return render_template("login.html")

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        # find company's stock and take share number
        stock = lookup(request.form.get("symbol"))
        shares = request.form.get("shares")
        
        # if stock doesnt exist
        if not stock:
            return apology("Invalid Symbol")
            
        #shares are not entered
        if not shares:
            return apology("missing shares")
            
        # check for the stock whether user have it
        stock_raw = db.execute("SELECT * FROM transactions WHERE id = :id and symbol = :symbol",
                            id=session["user_id"], symbol=stock['symbol'])
        if not stock_raw:
            return apology("you do not own this stock")            
        
        #convert shares str to int and check validity     
        share_number = int (shares)
        if share_number <= 0:
            return apology("you must give me valid share numbers")

        #search database and record shares
        shares_raw = db.execute("SELECT sum(quantity) FROM transactions WHERE id = :id and symbol = :symbol",
                            id=session["user_id"], symbol=stock['symbol'])
        user_shares = shares_raw[0]["sum(quantity)"]
        
        # share number can not be greater than user's own shares
        if share_number > user_shares:
            return apology("not enough owned shares")
            
        # stock variables
        stock_price = stock['price']
        stock_name = stock['name']
        stock_symbol = stock['symbol']
        
        # total share value
        share_price = stock_price*share_number
        
        # query database for username
        user_row = db.execute("SELECT * FROM users WHERE id = :id", 
                            id=session["user_id"])        
        user_cash = float (user_row[0]['cash'])
            
        # flash message
        flash("Sold!")    
            
        # update cash
        user_cash = user_cash + share_price
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", 
                    cash=user_cash, id=session["user_id"]) 
        
        # record transaction
        db.execute("INSERT INTO transactions (id, symbol, price, quantity, total) VALUES(:id, :symbol, :price, :quantity, :total)",
                    id=session["user_id"], symbol=stock_symbol, price=stock_price, quantity=-share_number, total=share_price)
        
        return redirect(url_for("index"))
        
    return render_template("sell.html")

@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """ Allow user to change password"""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure password was submitted
        if not request.form.get("old_password"):
            return apology("must provide old password")
        
        # ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password")
            
        # ensure new password check was submitted
        elif not request.form.get("new_password"):
            return apology("must provide new password check")            
        
        # ensure user didn't do typo    
        elif not request.form.get("new_password") == request.form.get("new_password2"):
            return apology("new passwords do not match", "you did typo then")
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        
        # check old password's validity
        old_password = request.form.get("old_password")
        check_pw = rows[0]["hash"]
        if not pwd_context.verify(old_password, check_pw):
            return apology("old password is incorrect")

        # hash new password
        new_password = request.form.get("new_password")
        new_hash = pwd_context.hash(new_password)
        
        result = db.execute("UPDATE users SET hash = :hash WHERE id = :id", 
                            hash=new_hash, id=session["user_id"])
        # database failed           
        if not result:
            return apology("can not update")
        
        # flash message
        flash("You changed your password!") 
            
        # redirect user to login page, because she/he succeeded
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("password.html")