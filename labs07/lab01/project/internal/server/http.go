package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"sync/atomic"
	"time"
)

var requestCount int64

func Handler(w http.ResponseWriter, r *http.Request) {
	count := atomic.AddInt64(&requestCount, 1)
	time.Sleep(100 * time.Millisecond)
	fmt.Fprintf(w, "Hello! Request #%d\n", count)
	log.Printf("Handled request #%d", count)
}

func StartServer() {
	mux := http.NewServeMux()
	mux.HandleFunc("/", Handler)
	
	server := &http.Server{
		Addr:    ":8080",
		Handler: mux,
	}
	
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, os.Interrupt)
	
	go func() {
		log.Println("Server starting on :8080")
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()
	
	<-stop
	log.Println("Shutting down server...")
	
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	if err := server.Shutdown(ctx); err != nil {
		log.Printf("Server shutdown error: %v", err)
	}
	
	log.Println("Server stopped")
}

func GetRequestCount() int64 {
	return atomic.LoadInt64(&requestCount)
}

