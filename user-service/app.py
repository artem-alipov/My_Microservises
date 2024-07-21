from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@postgres:5432/userdb"

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    age = Column(Integer)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

class UserService(user_pb2_grpc.UserServiceServicer):
    def AddUser(self, request, context):
        db = SessionLocal()
        existing_user = db.query(User).filter(User.id == request.id).first()
        if existing_user:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('User with this ID already exists')
            return user_pb2.UserResponse(message="User with this ID already exists")
        user = User(id=request.id, name=request.name, email=request.email, age=request.age)
        db.add(user)
        db.commit()
        db.close()
        return user_pb2.UserResponse(message="User added successfully")

    def GetUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.id == request.id).first()
        db.close()
        if user:
            return user_pb2.User(id=user.id, name=user.name, email=user.email, age=user.age)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.User()

    def UpdateUser(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.id == request.id).first()
        if user:
            user.name = request.name
            user.email = request.email
            user.age = request.age
            db.commit()
            db.close()
            return user_pb2.UserResponse(message="User updated successfully")
        else:
            db.close()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return user_pb2.UserResponse(message="User not found")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()