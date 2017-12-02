from flask import Flask, jsonify, Response

app = Flask(__name__)

sent = False

@app.route('/invest', methods=['POST'])
def index():
    global sent
    sent = True
    return Response(status=200, mimetype='application/json')

@app.route('/invest', methods=['GET'])
def signal():
    global sent
    if sent:
        #now back to square one
        sent = False
        return jsonify({'msg': 'yep it\'s time'})
    else:
        return jsonify({'msg': 'no sorry'})

if __name__ == '__main__':
    app.run(debug=True)


