package main

import (
	"fmt"
	//"math"
)

func main() {
	a := []int{1,2,3}
	b := []int{4,5,6}
	c := append(a,b...)
	fmt.Println(c)
}
