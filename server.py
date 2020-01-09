from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/testing', methods=['GET'])
def getTesting():
    return render_template('testing.html', text=request.args.get('link'))

@app.route('/j')
def root():
    return app.send_static_file('tf_idf_test.json')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD']= True
    app.run()
