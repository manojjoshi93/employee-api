from flask import request, Flask, jsonify
import requests
import json

# app = Flask(__name__)


base_url = 'https://8azq13jsqb.execute-api.us-east-1.amazonaws.com/Prod'

r = requests.post(f"{base_url}/employee", data=
	{'id':'1', 'name': 'Vicky', 'branch':'Toronto'})
print(r.content)


# r = requests.patch(f"{base_url}/employee/2", data={'name': 'Graham'})
# print(r.content)

# r = requests.delete(f"{base_url}/employee/1")
# print(r.content)

# Not required
# @app.route(f'/{base_url}/employee', methods=["POST"])
# def create_user():
# 	headers = {'Content-Type': 'application/json'}
# 	data = {'id':'1', 'name': 'Manoj', 'branch':'Toronto'}
# 	return jsonify(data), 201

# if __name__ == "__main__":
# 	app.run(debug=True)