package ding

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestDing(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/ding", nil)
	w := httptest.NewRecorder()

	Ding(w, req)

	resp := w.Result()
	body, err := io.ReadAll(resp.Body)
	defer resp.Body.Close()

	if err != nil {
		t.Errorf("Unexpected error while reading the body : %v", err)
	}

	if bodyStr := string(body) ; bodyStr != "Dong !" {
		t.Errorf("Expected body to be Dong ! but received %v", bodyStr)
	}
}