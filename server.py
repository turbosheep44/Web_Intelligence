from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods=['POST'])
def dashboardPost():

    postRequest = request.form
    source = postRequest['source']

    if source == 'big':
        pathModifier = 'output_json_big/'
        active = "big"
    else:
        pathModifier = 'output_json_small/'
        active = "small"
        print(pathModifier)

    return render_template("dashboard.html", active=active)


@app.route('/')
def dashboard():
    return render_template("dashboard.html", active="small")


@app.route('/placeholder')
def pgaeholder():
    return render_template("placeholder_page.html")


@app.route('/node', methods=['GET'])
def getNode():
    nodeId = request.args.get('id')
    nodeName = request.args.get('nodeName')

    json_path = "tfidfNode?id=" + nodeId
    return render_template('keywordCloud.html', json_path=json_path, nodeName=nodeName, nodeId=nodeId)


@app.route('/edge', methods=['GET'])
def getEdge():
    source = request.args.get('source')
    target = request.args.get('target')
    sourceName = request.args.get('sourceName')
    targetName = request.args.get('targetName')
    json_path = "tfidfEdge?source=" + source + "&target="+target
    return render_template('keywordCloud.html', json_path=json_path, sourceName=sourceName, targetName=targetName)


@app.route('/graph')
def graph():
    return app.send_static_file(pathModifier + 'graph.json')


@app.route('/graphStats')
def rootStats():
    return app.send_static_file(pathModifier + 'graph_stats.json')


@app.route('/details', methods=['GET'])
def rootdeatails():
    file_id = request.args.get('link')
    return app.send_static_file(pathModifier + 'node_data/'+file_id+'.json')


@app.route('/d')
def rootd():
    return app.send_static_file(pathModifier + 'details.json')


@app.route('/ex')
def ex():
    return render_template("force_connected.html")


@app.route('/exj')
def aaa():
    return app.send_static_file(pathModifier + 'got_social_graph.json')


@app.route('/tfidfEdge', methods=['GET'])
def mroot():
    source = request.args.get('source')
    target = request.args.get('target')
    return app.send_static_file(pathModifier + 'tf_idf_edges/'+source + '_' + target + '.json')


@app.route('/tfidfNode', methods=['GET'])
def noderoot():
    nodeId = request.args.get('id')
    return app.send_static_file(pathModifier + 'tf_idf_nodes/'+nodeId+'.json')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, 'public, max-age=0'"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r


if __name__ == '__main__':
    global pathModifier
    pathModifier = 'output_json_small/'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
