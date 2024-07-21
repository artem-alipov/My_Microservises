import os
from flask import Flask, request, jsonify
import grpc
import user_pb2
import user_pb2_grpc
import order_pb2
import order_pb2_grpc

app = Flask(__name__)

USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'user-service:50051')
ORDER_SERVICE_URL = os.getenv('ORDER_SERVICE_URL', 'order-service:50052')

@app.route('/v1/user/create', methods=['POST'])
def create_user():
    data = request.json
    with grpc.insecure_channel(USER_SERVICE_URL) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        user = user_pb2.User(id=data['id'], name=data['name'], email=data['email'], age=data['age'])
        try:
            response = stub.AddUser(user)
            return jsonify({'message': response.message})
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                 return jsonify({'message': 'User with this ID already exists'}), 409
            else:
                return jsonify({'message': 'Internal server error'}), 500

@app.route('/v1/user/update', methods=['PUT'])
def update_user():
    data = request.json
    with grpc.insecure_channel(USER_SERVICE_URL) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        user = user_pb2.User(id=data['id'], name=data['name'], email=data['email'], age=data['age'])
        try:
            response = stub.UpdateUser(user)
            return jsonify({'message': response.message})
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return jsonify({'message': 'User not found'}), 404
            else:
                return jsonify({'message': 'Internal server error'}), 500

@app.route('/v1/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    with grpc.insecure_channel(USER_SERVICE_URL) as channel:
        stub = user_pb2_grpc.UserServiceStub(channel)
        user_request = user_pb2.UserId(id=user_id)
        try:
            user_response = stub.GetUser(user_request)
            if user_response.id:
                return jsonify({
                    'id': user_response.id,
                    'name': user_response.name,
                    'email': user_response.email,
                    'age': user_response.age
                })
            else:
                return jsonify({'message': 'User not found'}), 404
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return jsonify({'message': 'User not found'}), 404
            else:
                return jsonify({'message': 'Internal server error'}), 500
          
@app.route('/v1/order/create', methods=['POST'])
def create_order():
    data = request.json
    with grpc.insecure_channel(ORDER_SERVICE_URL) as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)
        order = order_pb2.Order(id=data['id'], title=data['title'], description=data['description'], user_id=data['user_id'])
        try:
            response = stub.CreateOrder(order)
            return jsonify({'message': response.message})
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                return jsonify({'message': 'Order with this ID already exists'}), 409
            elif e.code() == grpc.StatusCode.NOT_FOUND:
                return jsonify({'message': 'User not found'}), 404
            else:
                return jsonify({'message': 'Internal server error'}), 500

@app.route('/v1/order/update', methods=['PUT'])
def update_order():
    data = request.json
    with grpc.insecure_channel(ORDER_SERVICE_URL) as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)
        order = order_pb2.Order(id=data['id'], title=data['title'], description=data['description'], user_id=data['user_id'])
        try:
            response = stub.UpdateOrder(order)
            return jsonify({'message': response.message})
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return jsonify({'message': 'Order not found'}), 404
            else:
                return jsonify({'message': 'Internal server error'}), 500

@app.route('/v1/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    with grpc.insecure_channel(ORDER_SERVICE_URL) as channel:
        stub = order_pb2_grpc.OrderServiceStub(channel)
        order_request = order_pb2.OrderId(id=order_id)     
        try:
            order_response = stub.GetOrder(order_request)
            if order_response.id:
                return jsonify({
                    'id': order_response.id,
                    'title': order_response.title,
                    'description': order_response.description,
                    'user_id': order_response.user_id
            })
            else:
                return jsonify({'message': 'Order not found'}), 404
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return jsonify({'message': 'Order not found'}), 404
            else:
                return jsonify({'message': 'Internal server error'}), 500
                            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7070)