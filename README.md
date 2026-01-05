# Natural Language to SQL

This tool helps users / non-programmers to get data from a DB using natural language.

## Install the Necessary Packages

All the necessary Python pacakges are added to the [requirements.txt](/services/requirements.txt) file. Run the below command to install all the packages from this file.

```bash
pip3 install -r requirements.txt
```

The below command installs the necessary Go gRPC packages.

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Add the installed Go protoc-gen-go package to PATH

```bash
export PATH="$PATH:$(go env GOPATH)/bin"
```

## Generate the gRPC Files

Run the below command from the /backend folder to generate the Python gRPC files.

```bash
python3 -m grpc_tools.protoc -I./proto --python_out=./services/proto --grpc_python_out=./services/proto ./proto/service.proto
```

Run the below command from the /backend folder to generate the Go gRPC files.

```bash
protoc --proto_path=./proto --go_out=./api/proto --go_opt=paths=source_relative --go-grpc_out=./api/proto --go-grpc_opt=paths=source_relative ./proto/service.proto
```

## API Usage

### Request

```bash
curl --location 'http://localhost:8080/api/query' \
--header 'Content-Type: application/json' \
--data '{
    "query": "Give me the top 3 customer who has ordered the most number of items along with the total number of orders for each"
}'
```

### Response

```bash
{
  "isSuccess": true,
  "columns": [
    "id",
    "name",
    "distinct_orders"
  ],
  "rows": [
    {
      "distinct_orders": 3,
      "id": 1,
      "name": "Alice Johnson"
    },
    {
      "distinct_orders": 2,
      "id": 3,
      "name": "Carol White"
    },
    {
      "distinct_orders": 2,
      "id": 6,
      "name": "Featherington"
    }
  ],
  "metadata": {
    "sqlQuery": "SELECT c.id, c.name, COUNT(DISTINCT o.id) AS distinct_orders\nFROM customers c\nINNER JOIN orders o ON c.id = o.customer_id\nGROUP BY c.id, c.name\nORDER BY distinct_orders DESC\nLIMIT 3;",
    "rowCount": 3
  }
}
```