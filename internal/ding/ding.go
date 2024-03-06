package ding

import (
	"fmt"
	"net/http"
)

func Ding(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Dong !")
}