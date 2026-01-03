package handlers

import (
	"fmt"
	"net/http"

	"github.com/ManoVikram/NL-To-SQL-With-AI/api/models"
	pb "github.com/ManoVikram/NL-To-SQL-With-AI/api/proto"
	"github.com/ManoVikram/NL-To-SQL-With-AI/api/services"
	"github.com/gin-gonic/gin"
)

func extractCell(cell *pb.Cell) any {
	switch value := cell.Value.(type) {
	case *pb.Cell_BoolValue:
		return value.BoolValue
	case *pb.Cell_IntValue:
		return value.IntValue
	case *pb.Cell_DoubleValue:
		return value.DoubleValue
	case *pb.Cell_BytesValue:
		return value.BytesValue
	case *pb.Cell_StringValue:
		return value.StringValue
	case *pb.Cell_IsNull:
		return nil
	default:
		return nil
	}
}

func extractColumns(pbColumns []*pb.Column) []string {
	if pbColumns == nil {
		return []string{}
	}

	columns := make([]string, len(pbColumns))

	for index, column := range pbColumns {
		columns[index] = column.Name
	}

	return columns
}

func extractRows(pbRows []*pb.Row, columns []string) []map[string]any {
	if pbRows == nil {
		return []map[string]any{}
	}

	rows := make([]map[string]any, len(pbRows))

	for rowIndex, row := range pbRows {
		rowData := make(map[string]any)

		for columnIndex, cell := range row.Cells {
			rowData[columns[columnIndex]] = extractCell(cell)
		}

		rows[rowIndex] = rowData
	}

	return rows
}

func QueryHandler(services *services.Service) gin.HandlerFunc {
	return func(c *gin.Context) {
		// Step 1 - Unmarshal the request body
		var request models.QueryRequest

		if err := c.ShouldBindJSON(&request); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": fmt.Sprintf("Invalid request body: %v", err.Error())})
			return
		}

		// Step 2 - Call the gRPC method to process the query
		gRPCResponse, err := services.Client.QueryDB(c.Request.Context(), &pb.QueryRequest{
			Query: request.Query,
		})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": fmt.Sprintf("Unable to process the query: %v", err.Error())})
			return
		}

		// Step 3 - Convert the gRPC response to HTTP response
		columns := extractColumns(gRPCResponse.Columns)
		rows := extractRows(gRPCResponse.Rows, columns)

		metadata := models.QueryMetadata{
			SQLQuery: gRPCResponse.Metadata.QueryGenerated,
			RowCount: int(gRPCResponse.Metadata.RowCount),
		}

		response := models.QueryResponse{
			IsSuccess:    gRPCResponse.IsSuccess,
			ErrorMessage: gRPCResponse.ErrorMessage,
			Columns:      columns,
			Rows:         rows,
			Metadata:     &metadata,
		}

		c.JSON(http.StatusOK, response)
	}
}
