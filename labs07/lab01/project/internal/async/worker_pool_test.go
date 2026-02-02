package async

import (
	"context"
	"sync"
	"testing"
	"time"
)

func TestWorkerPool_BasicFunctionality(t *testing.T) {
	pool := NewWorkerPool(3)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	tasks := []Task{
		{ID: 1, Data: "task1"},
		{ID: 2, Data: "task2"},
		{ID: 3, Data: "task3"},
	}
	
	go pool.Start(ctx)
	
	for _, task := range tasks {
		pool.Submit(task)
	}
	
	time.Sleep(2 * time.Second)
	pool.Stop()
	cancel()
	
	results := make(map[int]bool)
	for result := range pool.GetResults() {
		results[result.TaskID] = true
	}
	
	if len(results) != len(tasks) {
		t.Errorf("Expected %d results, got %d", len(tasks), len(results))
	}
}

func TestWorkerPool_ConcurrentSubmission(t *testing.T) {
	pool := NewWorkerPool(5)
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	var wg sync.WaitGroup
	totalTasks := 20
	
	go pool.Start(ctx)
	
	for i := 0; i < totalTasks; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			pool.Submit(Task{ID: id, Data: id})
		}(i)
	}
	
	wg.Wait()
	time.Sleep(1 * time.Second)
	pool.Stop()
	
	results := make(map[int]bool)
	for result := range pool.GetResults() {
		results[result.TaskID] = true
	}
	
	if len(results) < totalTasks/2 {
		t.Errorf("Expected at least %d results, got %d", totalTasks/2, len(results))
	}
}

