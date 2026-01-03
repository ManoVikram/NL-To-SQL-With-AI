package models

type QueryMetadata struct {
	SQLQuery string `json:"sqlQuery"`
	RowCount int    `json:"rowCount"`
}
