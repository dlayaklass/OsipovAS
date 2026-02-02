package main

import (
	"context"
	"fmt"
	"lab-async-go/internal/async"
	"lab-async-go/internal/server"
	"math/rand"
	"sync"
	"time"
)

func main() {
	fmt.Println("=== Лабораторная работа: Асинхронное программирование в Go ===")
	
	var wg sync.WaitGroup
	
	// 1. Базовые горутины
	fmt.Println("\n1. Базовые горутины:")
	wg.Add(5)
	for i := 1; i <= 5; i++ {
		go async.Worker(i, &wg)
	}
	wg.Wait()
	fmt.Println("All workers completed")
	
	// 2. Каналы
	fmt.Println("\n2. Каналы:")
	ch := make(chan int, 3)
	go async.Producer(ch)
	async.Consumer(ch)
	
	// 3. Worker Pool
	fmt.Println("\n3. Worker Pool:")
	rand.Seed(time.Now().UnixNano())
	pool := async.NewWorkerPool(3)
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	go pool.Start(ctx)
	
	for i := 1; i <= 10; i++ {
		pool.Submit(async.Task{ID: i})
	}
	
	go func() {
		time.Sleep(5 * time.Second)
		pool.Stop()
		cancel()
	}()
	
	for result := range pool.GetResults() {
		fmt.Printf("Result: %s\n", result.Output)
	}
	
	// 4. HTTP сервер
	fmt.Println("\n4. HTTP Сервер:")
	fmt.Println("Запуск сервера на http://localhost:8080")
	fmt.Println("Нажмите Ctrl+C для остановки")
	go server.StartServer()
	
	select {
	case <-time.After(30 * time.Second):
		fmt.Println("Демонстрация завершена")
	}
}

