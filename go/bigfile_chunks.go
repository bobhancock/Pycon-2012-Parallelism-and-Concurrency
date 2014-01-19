package main

import (
	"bigfile"
	"fmt"
	"log"
	"os"
	"strings"
	"strconv"
	"runtime"
)

func main() {
	if len(os.Args) < 3 {
		log.Println("usage: settings_file howmany_chunks gomaxprocs")
		return 
	}
	// settings file
	sfile := os.Args[1]
	sfile = strings.Trim(sfile, "\" ")
	q := bigfile.Settings(sfile, "TARGET_USERNAME")
	q = strings.Trim(q, "\"")
//	fmt.Printf("1=%s\n",q)

	max_procs, err := strconv.Atoi(os.Args[3])
	runtime.GOMAXPROCS(max_procs)

	// source data file
	bf := bigfile.Settings(sfile, "BIG_FILE")
	bf = strings.Trim(bf, "\" ")
	//fmt.Printf("bigfile=%s\n", bf)

	// how many chunks should the file be divided into?
	num_chunks, err := strconv.Atoi(os.Args[2])
	if err != nil {
		log.Fatalf("Could not convert %s to and int.\n", os.Args[2])
	}

	// get chunk parameters
	f, err := os.Open(bf)
	if err != nil {
		log.Fatalf("Cannot open %s.\n", bf)
	}
		
	// chunks is an array of []int where each []int contains
	// the start byte and the size of each chunk.
	chunks_ar := bigfile.SizeChunks(f, int64(num_chunks) )
	fmt.Println("chunks_ar=", chunks_ar)
	f.Close()
	

	// For each chunk launch the search for the matching string
	// in a separate go routine.
	results := make(chan []int)
	var recsmatch int
	var recsread int

	for i := 0; i < num_chunks; i++ {
		f, err := os.Open(bf)
		if err != nil {
			log.Fatalf(fmt.Sprintf("Could not open %s on iteration %d: %v\n", bf, i, err))
		}
		defer f.Close()
		//FindString(f *os.File, start, chunksize int64, query string, done chan int) {
		chunk_start := chunks_ar[i][0]
		chunk_size := chunks_ar[i][1]
		go bigfile.FindString(f, chunk_start,chunk_size, q, results, i)
	}

	for i := 0; i < num_chunks; i++ {
		//recs := make([]int, 2)
		recs :=  <- results
		recsread += recs[0]
		recsmatch += recs[1]
	}
	fmt.Println(recsread,recsmatch)
}