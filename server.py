from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")


# just in case you need some primes
# [x for x in range(10000) if len([j for j in range(2, x) if x % j == 0]) < 1]


if __name__ == '__main__':
    app.run()
