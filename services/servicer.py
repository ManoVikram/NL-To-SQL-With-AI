import logging
from proto import service_pb2, service_pb2_grpc
from pipeline.query_pipeline import QueryPipeline

logger = logging.getLogger(__name__)


class NLToSQLServicer(service_pb2_grpc.NLToSQLServiceServicer):
    def __init__(self, pipeline: QueryPipeline):
        super().__init__()
        self.pipeline = pipeline

    def _prepare_cell(self, value):
        if value is None:
            return service_pb2.Cell(is_null=True)
        elif isinstance(value, bool):
            return service_pb2.Cell(bool_value=value)
        elif isinstance(value, int):
            return service_pb2.Cell(int_value=value)
        elif isinstance(value, float):
            return service_pb2.Cell(double_value=value)
        elif isinstance(value, bytes):
            return service_pb2.Cell(bytes_value=value)
        else:
            return service_pb2.Cell(string_value=str(value))

    def _prepare_columns(self, columns):
        return [
            service_pb2.Column(
                name=column["name"],
                type=column["data_type"],
                is_nullable=column.get("is_nullable", True)
            )
            for column in columns
        ]

    def _prepare_rows(self, rows):
        proto_rows = []
        
        for row in rows:
            cells = []    
            for column_value in row:
                cell = self._prepare_cell(column_value)
                cells.append(cell)
            proto_rows.append(service_pb2.Row(cells=cells))

        return proto_rows

    def QueryDB(self, request, context):
        try:
            # Step 1 - Retrieve the user query from the request
            query = request.query
            logging.info(f"Received query: {query}")

            # Step 2 - Execute the pipeline to convert the natural language query to SQL and execute it and return the results
            result = self.pipeline.execute(user_query=query)

            # Step 3 - Construct the gRPC response
            proto_columns = self._prepare_columns(result["results"]["columns"])
            proto_rows = self._prepare_rows(result["results"]["rows"])

            return service_pb2.QueryResponse(
                is_success=result["is_success"],
                error_message=result["error"] if result["error"] else "",
                columns=proto_columns,
                rows=proto_rows,
                metadata=service_pb2.QueryMetadata(
                    query_generated=result["sql_query"],
                    row_count=len(proto_rows)
                )
            )
        except Exception as error:
            logging.error(f"Error processing query: {error}", exc_info=True)
            return service_pb2.QueryResponse(
                is_success=False,
                error_message=str(error),
                columns=[],
                rows=[],
                metadata=service_pb2.QueryMetadata(
                    query_generated="",
                    row_count=0
                )
            )