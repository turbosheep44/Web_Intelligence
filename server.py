from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/g')
def g():
    return render_template("web.html")


@app.route('/j')
def root():
    return app.send_static_file('email.json')


@app.route('/ex')
def ex():
    return render_template("force_connected.html")

@app.route('/exj')
def aaa():
    return app.send_static_file('got_social_graph.json')
    

# just in case you need some primes
# [x for x in range(10000) if len([j for j in range(2, x) if x % j == 0]) < 1]


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
