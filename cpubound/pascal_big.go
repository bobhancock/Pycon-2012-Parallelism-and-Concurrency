package main

import (
//    "fmt"
    "math"
	"os"
	"flag"
	"log"
	"big"
	"runtime/pprof"
)

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")
var memprofile = flag.String("memprofile", "", "write memory profile to this file")
var nrows = flag.Int("nrows", 10, "number of rows to calculate")

// Reverse the slice
func reverse(r []*big.Int) []*big.Int {
	n, h := len(r), len(r)/2
	for i := 0; i < h; i++ {
       		r[i], r[n-1-i] = r[n-1-i], r[i]
	}
	return r
}

func main() {
	flag.Parse()
	m := int64(*nrows)

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


	prev := make([]*big.Int, 1)
	one := big.NewInt(int64(1)) 
	prev[0] = one
	x := big.NewInt(int64(0))

    for row := int64(1); row < m; row++ {
		curr := make([]*big.Int,1,row+1)
		curr[0] = one

		mid := int64(row/2) + 1 
		var right int64 
		if math.Fmod(float64(row), 2.0) == 0 {
			right = mid - 1
		} else {
			right = mid
		}
		
		for j := int64(1); j < mid; j++ {
			x = x.Add(prev[j - 1], prev[j])
			curr = append(curr, x)
			x = big.NewInt(int64(0))
		}

		// Take a slice of the first half of the row, reverse it, and
		// append to the current row.
		s := make([]*big.Int, right)
		r := curr[0:right]
		copy(s,r)
		rev := reverse(s)
		curr = append(curr, rev...)
		//fmt.Println(curr)

		prev = curr[:]
    }
 }