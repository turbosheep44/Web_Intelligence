from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/placeholder')
def pgaeholder():
    return render_template("placeholder_page.html")


@app.route('/node', methods=['GET'] )
def getNode():
    nodeId = request.args.get('id')
    nodeName = request.args.get('nodeName')

    json_path = "tfidfNode?id=" + nodeId 
    return render_template('keywordCloud.html', json_path = json_path, nodeName = nodeName, nodeId = nodeId )
    # return app.send_static_file('tf_idf/'+source + '_' + target +'.json')


@app.route('/edge', methods=['GET'] )
def getEdge():
    source = request.args.get('source')
    target = request.args.get('target')
    sourceName = request.args.get('sourceName')
    targetName = request.args.get('targetName')
    json_path = "tfidfEdge?source=" + source + "&target="+target
    return render_template('keywordCloud.html', json_path = json_path, sourceName=sourceName, targetName=targetName)


@app.route('/g')
def g():
    return render_template("web.html")


@app.route('/j')
def root():
    return app.send_static_file('graph.json')

@app.route('/graphStats')
def rootStats():
    return app.send_static_file('graph_stats.json')

@app.route('/details', methods=['GET'] ) 
def rootdeatails():
    file_id = request.args.get('link')
    # with ope')
    return app.send_static_file('node_data/'+file_id+'.json')


@app.route('/d')
def rootd():
    return app.send_static_file('details.json')


@app.route('/ex')
def ex():
    return render_template("force_connected.html")

@app.route('/exj')
def aaa():
    return app.send_static_file('got_social_graph.json')
    

@app.route('/tfidfEdge', methods=['GET'])
def mroot():
    source = request.args.get('source')
    target = request.args.get('target')
    return app.send_static_file('tf_idf_edges/'+source + '_' + target +'.json')

    
@app.route('/tfidfNode', methods=['GET'])
def noderoot():
    nodeId = request.args.get('id')
    return app.send_static_file('tf_idf_nodes/'+nodeId+'.json')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
