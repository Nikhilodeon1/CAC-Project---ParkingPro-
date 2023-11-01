from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, abort
import json
import requests
import os.path
from roboflow import Roboflow
from werkzeug.utils import secure_filename
app = Flask(__name__)
#app.run(debug=True)
app.secret_key = "|\|||<|-|||_"

#<!--/progress /aibot /music /you /logbook-->

@app.route('/', methods=['GET', 'POST'])
def home():
  if session:
    return redirect(url_for('destination'))
  else:
    return render_template('home.html')

@app.route('/p', methods=['POST'])
def p():
  long = request.form['long']
  lat = request.form['lat']
  # Define the zoom level and image size
  zoom = 20 # 1-20
  size = 640 # 1-640

  # Define the base URL for Bing Maps API
  base_url = "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial"

  # Construct the full URL with parameters
  full_url = f"{base_url}/{lat},{long}/{zoom}?mapSize={size},{size}&key=AldazXMMRfAD8Jg5w-XqpXM7wFjNP1poTOP52Q8LViFaRiqPofN2e8wWgonN0SHu"

  # Get the image response from the API
  response = requests.get(full_url)

  # Check if the response is successful
  if response.status_code == 200:
      # Save the image to a file
      with open("satellite_image.jpg", "wb") as f:
          f.write(response.content)

  rf = Roboflow(api_key="4RuIXtKeuz8R4qIyL19Y")
  project = rf.workspace().project("pl-psq41")
  model = project.version(1).model

  # infer on a local image
  result = model.predict("satellite_image.jpg", confidence=0, overlap=30).json()
  print(result)
  print(len(result['predictions']))
  print("DOOOOOOOONEEEEEEEEEE")
  if len(result['predictions']) > 0:
    session['lat']=lat
    session['long']=long
    return redirect(url_for('destination'))
  else:
    return redirect(url_for('home'))

@app.route('/destination', methods=['GET', 'POST'])
def destination():
  if session:
    return render_template('destination.html', lat=session['lat'], long=session['long'])
  else:
    return redirect(url_for('home'))

@app.route('/delsession', methods=['GET', 'POST'])
def delsession():
  session.clear()
  return redirect(url_for('home'))

app.run(host='0.0.0.0', port=81)
