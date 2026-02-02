package async

import (
	"context"
	"testing"
	"time"
)

func TestBufferedChannelProcessor(t *testing.T) {
	input := make(chan int, 5)
	
	for i := 1; i <= 5; i++ {
		input <- i
	}
	close(input)
	
	output := BufferedChannelProcessor(input, 3)
	
	expected := []int{2, 4, 6, 8, 10}
	var results []int
	
	for val := range output {
		results = append(results, val)
	}
	
	if len(results) != len(expected) {
		t.Errorf("Expected %d results, got %d", len(expected), len(results))
	}
	
	for i, val := range results {
		if val != expected[i] {
			t.Errorf("Expected %d at position %d, got %d", expected[i], i, val)
		}
	}
}

func TestChannelTimeout(t *testing.T) {
	ch := make(chan int)
	
	select {
	case <-ch:
		t.Error("Should not receive from channel")
	case <-time.After(100 * time.Millisecond):
		// Ожидаемое поведение - таймаут
	}
}

