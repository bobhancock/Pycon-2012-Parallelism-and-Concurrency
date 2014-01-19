package main

import (
	"time"
	"fmt"
	"stats"
)

func main() {
	s := time.Seconds()
	n := time.Nanoseconds()
	fmt.Println(s)
	fmt.Println(n)

	a := time.Nanoseconds()
	time.Sleep(2*1e9)
	b := time.Nanoseconds()
	e := b - a
	fmt.Println(float64(e) * 1e-9)
	
	d := []float64{1,2,3}
	fmt.Println(stats.StatsSampleStandardDeviation(d))
	
}