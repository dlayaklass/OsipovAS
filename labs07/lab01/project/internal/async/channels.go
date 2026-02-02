package async

import (
	"context"
	"fmt"
	"time"
)

func Producer(ch chan<- int) {
	for i := 0; i < 10; i++ {
		ch <- i
		fmt.Printf("Produced: %d\n", i)
	}
	close(ch)
}

func Consumer(ch <-chan int) {
	for {
		select {
		case val, ok := <-ch:
			if !ok {
				fmt.Println("Channel closed")
				return
			}
			fmt.Printf("Consumed: %d\n", val)
			time.Sleep(500 * time.Millisecond)
		case <-time.After(2 * time.Second):
			fmt.Println("Timeout occurred")
			return
		}
	}
}

func MergeChannels(ctx context.Context, chs ...<-chan int) <-chan int {
	out := make(chan int)
	
	for _, ch := range chs {
		go func(c <-chan int) {
			defer close(out)
			for {
				select {
				case val, ok := <-c:
					if !ok {
						return
					}
					select {
					case out <- val:
					case <-ctx.Done():
						return
					}
				case <-ctx.Done():
					return
				}
			}
		}(ch)
	}
	
	return out
}

func BufferedChannelProcessor(input <-chan int, bufferSize int) <-chan int {
	output := make(chan int, bufferSize)
	
	go func() {
		defer close(output)
		for val := range input {
			output <- val * 2
		}
	}()
	
	return output
}

