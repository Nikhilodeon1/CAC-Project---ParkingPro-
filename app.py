from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, abort
import json
import os.path
from werkzeug.utils import secure_filename
app = Flask(__name__)
#app.run(debug=True)
app.secret_key = "|\|||<|-|||_"

#<!--/progress /aibot /music /you /logbook-->

@app.route('/', methods=['GET', 'POST'])
def home():
  if session:
    return render_template('main2.html')
  else:
    return render_template('main.html')

@app.route('/progress', methods=['GET', 'POST'])
def progress():
  if session:
    return render_template('progress.html')
  else:
    return redirect(url_for('login'))

@app.route('/aibot', methods=['GET', 'POST'])
def aibot():
  if session:
    return render_template('aibot.html')
  else:
    return redirect(url_for('login'))
    
@app.route('/music', methods=['GET', 'POST'])
def music():
  if session:
    return render_template('music.html')
  else:
    return redirect(url_for('login'))
    
@app.route('/you', methods=['GET', 'POST'])
def you():
  if session:
    return render_template('you.html')
  else:
    return redirect(url_for('login'))
  
@app.route('/logbook', methods=['GET', 'POST'])
def logbook():
  if session:
    return render_template('logbook.html')
  else:
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  return render_template('login.html')

@app.route('/newacc', methods=['GET', 'POST'])
def newacc():
  return render_template('newacc.html')

@app.route('/setsession', methods=['GET', 'POST'])
def setsession():
  uname = request.form['uname']
  psw = request.form['psw']
  if request.form['from'] == "login":
    if os.path.isfile('users/'+uname+'.json'):
      f = open('users/'+uname+'.json')
      data = json.load(f)
      f.close()
      if data['psw'] == psw:
        session['uname'] = uname
        session['psw'] = psw
        return redirect(url_for('home'))

      else:
        flash('Wrong password')
        return redirect(url_for('login'))
    else:
      flash('User not found')
      return redirect(url_for('login'))
  else:
    with open("users/" + uname + ".json", "w") as file:
      dicta= {'psw': psw}
      json.dump(dicta, file)
      session['uname'] = uname
      session['psw'] = psw
      return redirect(url_for('home'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
  session.clear()
  return redirect(url_for('home'))
app.run(host='0.0.0.0', port=81)
