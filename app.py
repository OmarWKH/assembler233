'''
Packages:
flask
'''

# refer to registers with r
# link code

import assembler233 as ass
from flask import Flask, render_template, request # web framework @ http://flask.pocoo.org/
import os # for env variables

app = Flask(__name__, template_folder='.') # the Flask app will find event.html template in current folder
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

## Views ##
@app.route('/', methods=['GET', 'POST'])
def assemble():
    if request.method == 'GET':
        return render_template('index.html', asm_text='set 5')
    elif request.method == 'POST':
        asm = request.form['asm']
        binary = ass.assemble(asm)
        hexd = ass.binary_to_hex(binary)
        return render_template('index.html', asm_text=asm, binary_text=binary, hexd_text=hexd)
        
@app.route('/do')
def do():
    return "hi"

## Run ##
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	host = os.environ.get('IP', '0.0.0.0') # port and host are to run on cloud9, remove if running locally
	app.run(host=host, port=port, debug=False)
