package main

import (
    "fmt"
    "math"
	"os"
	"flag"
	"log"
	"strconv"
	"runtime/pprof"
)

var maxint64 = int64(9223372036854775807)

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")
var memprofile = flag.String("memprofile", "", "write memory profile to this file")

// Reverse the slice
func reverse(r []int64) []int64 {
	n, h := len(r), len(r)/2
	for i := 0; i < h; i++ {
		r[i], r[n-1-i] = r[n-1-i], r[i]
	}
	return r
}

func main() {
	if len(os.Args) < 2 {
		log.Fatalf("usage: %s iterations\n", os.Args[0])
	}

	flag.Parse()
	//Setup  profiling
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	if *memprofile != "" {
        f, err := os.Create(*memprofile)
        if err != nil {
            log.Fatal(err)
        }
        pprof.WriteHeapProfile(f)
        f.Close()
        return
    }

	m, err := strconv.Atoi(os.Args[1]) //max iterations
	if err != nil {
		log.Fatalf("Could not convert %s to int.\n", os.Args[1])
	}
	one := int64(1)
	prev := []int64{one}
    //fmt.Println(prev)

    for row := 1; row < m; row++ {
		curr := make([]int64,1,row)
		curr[0] = one

		mid := (row / 2) 
		var right int 
		if math.Fmod(float64(row), 2.0) == 0 {
			right = mid
		} else {
			right = mid + 1
		}
		
		for j := 1; j < mid; j++ {
			x :=  int64(prev[j - 1] + prev[j])
//			if int64(x) > maxint64 {
			if int64(x) < 0 {
//				log.Fatalf("row %d point %d exceed maxint64:%e  value:%d\n",row, j, maxint64, prev[j])
				log.Fatalf("row %d point %d value:%e\n",row, j, x)
			}
			
			curr = append(curr, x)
		}
		
		s := make([]int64, right)
		r := curr[0:right]
		copy(s,r)
		rev := reverse(s)
		curr = append(curr, rev...)
//		fmt.Println(curr)
		prev = curr
    }
	fmt.Printf("row: %d row_len: %d\n", prev, len(prev))
//prev[:len(prev)/2])
 }