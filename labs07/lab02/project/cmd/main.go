package main

import (
	"context"
	"fmt"
	"lab-async-go/internal/async"
	"lab-async-go/internal/server"
	"sync"
	"time"
)

func main() {
	fmt.Println("=== Лабораторная работа: Тестирование асинхронного кода в Go ===")
	fmt.Println("\nДля запуска тестов выполните:")
	fmt.Println("  go test ./... -v")
	fmt.Println("  go test ./... -race")
	fmt.Println("  go test ./... -cover")
	
	fmt.Println("\nДемонстрация компонентов:")
	
	// Демонстрация Counter
	fmt.Println("\n1. Counter:")
	counter := &async.Counter{}
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			counter.Increment()
		}()
	}
	wg.Wait()
	fmt.Printf("Counter value: %d\n", counter.Value())
	
	// Демонстрация каналов
	fmt.Println("\n2. Каналы:")
	ch := make(chan int, 3)
	go async.Producer(ch)
	time.Sleep(2 * time.Second)
	
	// Демонстрация Worker Pool
	fmt.Println("\n3. Worker Pool:")
	pool := async.NewWorkerPool(2)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	go pool.Start(ctx)
	
	for i := 1; i <= 5; i++ {
		pool.Submit(async.Task{ID: i})
	}
	
	time.Sleep(2 * time.Second)
	pool.Stop()
	
	// Демонстрация HTTP сервера
	fmt.Println("\n4. HTTP Server:")
	fmt.Println("Для тестирования HTTP сервера используйте тесты")
	fmt.Println("  go test ./internal/server/... -v")
}

