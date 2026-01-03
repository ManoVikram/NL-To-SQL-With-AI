package models

type QueryResponse struct {
	IsSuccess    bool             `json:"isSuccess"`
	ErrorMessage string           `json:"errorMessage,omitempty"`
	Columns      []string         `json:"columns,omitempty"`
	Rows         []map[string]any `json:"rows,omitempty"`
	Metadata     *QueryMetadata   `json:"metadata,omitempty"`
}
