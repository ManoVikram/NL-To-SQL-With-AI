from proto import service_pb2_grpc

class NLToSQLServicer(service_pb2_grpc.NLToSQLServiceServicer):
    def __init__(self):
        super().__init__()

    def QueryDB(self, request, context):
        query = request.query

        # Enhance the query > SQL generation > Validate the SQl > Execute the SQL and fetch the results