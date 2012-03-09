package main

import (
	"os"
	"io"
	"log"
	"fmt"
	"bufio"
)

func CreateTestFile(name string) {
	rec := []byte("012345678Z\nabcdZfghij\nklmnopqrsZ\n")

	fh, err := os.Create(name)
	if err != nil {
		log.Fatalf("testfile: %s\n", err)
		os.Exit(1)
	}
	defer fh.Close()
	fh.Write(rec)
}

func OpenTestFile(name string) *os.File {
	f, err := os.Open(name)
    if f == nil {
        fmt.Printf("can't open file; err=%s\n", err.String())
        os.Exit(1)
    }		
	if err != nil {
		log.Fatalf("Error opening %s\n", name)
		os.Exit(1)
	}
	return f
}

func main() {
	tfile := "/tmp/seektest"
	CreateTestFile(tfile)
	f := OpenTestFile(tfile)

	rs := io.ReadSeeker(f)
	start := int64(6)
	offset, err := rs.Seek(start, 0)
	if err != nil {
		log.Fatalf("FindString: error on seek-%n", err.String())
		os.Exit(1)
	}
	if offset != start {
		log.Fatalf("Expected offset of %d and received %d\n", start, offset)
	} else {
		fmt.Printf("Offset = %d\n", offset)
	}

	reader := bufio.NewReader(rs)
	line,_, _ := reader.ReadLine()
	fmt.Println(string(line))
}