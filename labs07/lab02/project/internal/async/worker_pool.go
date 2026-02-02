package async

import (
	"context"
	"fmt"
	"math/rand"
	"sync"
	"time"
)

type Task struct {
	ID   int
	Data interface{}
}

type Result struct {
	TaskID int
	Output string
}

type WorkerPool struct {
	workersCount int
	tasks        chan Task
	results      chan Result
	wg           sync.WaitGroup
}

func NewWorkerPool(workers int) *WorkerPool {
	return &WorkerPool{
		workersCount: workers,
		tasks:        make(chan Task, workers*2),
		results:      make(chan Result, workers*2),
	}
}

func (wp *WorkerPool) Start(ctx context.Context) {
	for i := 1; i <= wp.workersCount; i++ {
		wp.wg.Add(1)
		go func(workerID int) {
			defer wp.wg.Done()
			for {
				select {
				case task, ok := <-wp.tasks:
					if !ok {
						return
					}
					fmt.Printf("Worker %d processing task %d\n", workerID, task.ID)
					time.Sleep(time.Duration(rand.Intn(1000)) * time.Millisecond)
					wp.results <- Result{
						TaskID: task.ID,
						Output: fmt.Sprintf("Task %d completed by worker %d", task.ID, workerID),
					}
				case <-ctx.Done():
					return
				}
			}
		}(i)
	}
}

func (wp *WorkerPool) Submit(task Task) {
	wp.tasks <- task
}

func (wp *WorkerPool) GetResults() <-chan Result {
	return wp.results
}

func (wp *WorkerPool) Stop() {
	close(wp.tasks)
	wp.wg.Wait()
	close(wp.results)
}

