import os
from concurrent.futures import ThreadPoolExecutor

import grpc
from dotenv import load_dotenv

from proto import service_pb2, service_pb2_grpc


class NLToSQLServicer(service_pb2_grpc.NLToSQLServiceServicer):
    def __init__(self):
        super().__init__()

    def QueryDB(self, request, context):
        pass

def serve():
    # Step 1 - Load the environment variables
    load_dotenv()
    assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY is not set in the environment variables. Please add it to the environment variables file."
    assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY is not set in the environment variables. Please add it to the environment variables file."

    # Step 2 - Set up the gRPC server
    server = grpc.server(thread_pool=ThreadPoolExecutor(max_workers=10))

    # Step 3 - Add the servicer to the gRPC server
    service_pb2_grpc.add_NLToSQLServiceServicer_to_server(servicer=NLToSQLServicer(), server=server)

    # Step 4 - Bind the server to a port
    grpc_port = os.getenv("GRPC_PORT", 50051)
    server.add_insecure_port(f"[::]:{grpc_port}")

    # Step 5 - Start the gRPC server
    server.start()

    # Step 6 - Wait for termination
    server.wait_for_termination()

if __name__ == "__main__":
    serve()