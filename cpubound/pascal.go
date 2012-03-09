package main

import (
       "fmt"
)

func main() {
     m := 10000
     prev := []int{1}
     //fmt.Println(prev)
     for i := 0; i < m; i++ {
     	 curr := []int{1}
	 for j := 1; j < i; j++ {
	     curr = append(curr, prev[j - 1] + prev[j])
	 }
	 curr = append(curr, 1)
	 //fmt.Println(curr)
	 prev = curr
    }
    fmt.Println("Done")
}