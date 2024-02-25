from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        data = request.json 
        print("Received data:", data)
        return jsonify({'message': 'Success'}), 200
    else:
        return jsonify({'error': 'Only POST requests are allowed'}), 405  


if __name__ == '__main__':
    app.run(debug=True , port = 5555)
