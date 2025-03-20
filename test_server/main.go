package main

import (
	"log"
	"net/http"
)

func main() {
	const port = "8080"
	const filepathRoot = "api/"

	mux := http.NewServeMux()

	fsHandler := http.StripPrefix("/api", http.FileServer(http.Dir(filepathRoot)))
	mux.Handle("/api/", fsHandler)

	srv := http.Server{
		Addr:    ":" + port,
		Handler: mux,
	}

	log.Printf("Serving files from %s on port: %s\n", filepathRoot, port)
	log.Fatal(srv.ListenAndServe())
}
