
from flask import Flask, render_template, jsonify,\
	request, json, send_from_directory
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return render_template("home.html")


''' #If you want a favicon
@app.route('/favicon.ico') 
def favicon(): 
	return send_from_directory(os.path.join(app.root_path, 'static'), 'logo_blue.ico', mimetype='image/vnd.microsoft.icon')
  '''

if __name__ == '__main__':
    app.run(debug=True)
