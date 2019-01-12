from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
class tempdata:
    tempvalue = ''
@app.route('/', methods=['GET', 'POST'])
def basic_route():
    from datetime import datetime
    tempdata.tempvalue = datetime.now()
    request.form.get('timebut')
    if request.method == 'POST':
        form = request.form.get('timebut')
        tempdata.tempvalue = request.form.get('tempbut')
        return render_template('index.html', form=form)
    
    
    return render_template('index.html', form=tempdata.tempvalue)

app.run(host='0.0.0.0')
