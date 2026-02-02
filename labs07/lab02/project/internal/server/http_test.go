package server

import (
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
)

func TestHandler(t *testing.T) {
	req := httptest.NewRequest("GET", "/", nil)
	w := httptest.NewRecorder()
	
	Handler(w, req)
	
	resp := w.Result()
	body, _ := io.ReadAll(resp.Body)
	
	if resp.StatusCode != http.StatusOK {
		t.Errorf("Expected status 200, got %d", resp.StatusCode)
	}
	
	if len(body) == 0 {
		t.Error("Expected non-empty response body")
	}
}

func TestConcurrentRequests(t *testing.T) {
	req := httptest.NewRequest("GET", "/", nil)
	
	var wg sync.WaitGroup
	requests := 50
	
	for i := 0; i < requests; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			w := httptest.NewRecorder()
			Handler(w, req)
			if w.Code != http.StatusOK {
				t.Errorf("Expected status 200, got %d", w.Code)
			}
		}()
	}
	
	wg.Wait()
	
	if GetRequestCount() < int64(requests) {
		t.Errorf("Expected at least %d requests, got %d", requests, GetRequestCount())
	}
}

