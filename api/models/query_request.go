package models

type QueryRequest struct {
	Query string `json:"query" binding:"required"`
}