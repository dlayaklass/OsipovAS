package async

import (
	"fmt"
	"sync"
	"time"
)

func Worker(id int, wg *sync.WaitGroup) {
	defer wg.Done()
	fmt.Printf("Worker %d started\n", id)
	time.Sleep(time.Second)
	fmt.Printf("Worker %d completed\n", id)
}

type Counter struct {
	mu    sync.Mutex
	value int
}

func (c *Counter) Increment() {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value++
}

func (c *Counter) Value() int {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

func ProcessItems(items []int, processor func(int)) {
	var wg sync.WaitGroup
	for _, item := range items {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			processor(i)
			time.Sleep(10 * time.Millisecond)
		}(item)
	}
	wg.Wait()
}

