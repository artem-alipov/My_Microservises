from concurrent import futures
import grpc
import order_pb2
import order_pb2_grpc
import user_pb2
import user_pb2_grpc
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgres:5432/orderdb"
USER_SERVICE_URL = "user-service:50051"

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        db = SessionLocal()
        existing_order = db.query(Order).filter(Order.id == request.id).first()
        if existing_order:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Order with this ID already exists')
            return order_pb2.OrderResponse(message="Order with this ID already exists")

        with grpc.insecure_channel(USER_SERVICE_URL) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            user_request = user_pb2.UserId(id=request.user_id)
            user_response = stub.GetUser(user_request)
            if not user_response.id:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details('User not found')
                return order_pb2.OrderResponse(message="User not found")

        order = Order(id=request.id, title=request.title, description=request.description, user_id=request.user_id)
        db.add(order)
        db.commit()
        db.close()
        return order_pb2.OrderResponse(message="Order created successfully")

    def GetOrder(self, request, context):
        db = SessionLocal()
        order = db.query(Order).filter(Order.id == request.id).first()
        db.close()
        if order:
            return order_pb2.Order(id=order.id, title=order.title, description=order.description, user_id=order.user_id)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order not found')
            return order_pb2.Order()

    def UpdateOrder(self, request, context):
        db = SessionLocal()
        order = db.query(Order).filter(Order.id == request.id).first()
        if order:
            order.title = request.title
            order.description = request.description
            order.user_id = request.user_id
            db.commit()
            db.close()
            return order_pb2.OrderResponse(message="Order updated successfully")
        else:
            db.close()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order not found')
            return order_pb2.OrderResponse(message="Order not found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()