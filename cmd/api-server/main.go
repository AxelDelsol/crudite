package main

import (
	"fmt"
	"net/http"

	"github.com/axeldelsol/crudite/internal/ding"
)

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("GET /ding", ding.Ding)

	fmt.Println("Listening...")

	http.ListenAndServe(":8080", mux)
}