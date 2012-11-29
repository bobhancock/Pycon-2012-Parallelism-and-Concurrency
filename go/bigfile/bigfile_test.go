package bigfile

import (
	"testing"
	"os"
//	"io"
	"fmt"
	"log"
)

var tfile = "/tmp/chunktesting"
var cum int

func init() {
	CreateTestFile(tfile)
}

// testfile creates a text file for for testing chunk functionality
func CreateTestFile(name string) {
	rec := []byte("012345678Z\nabcdZfghij\nklmnopqrsZ\n")

	fh, err := os.Create(tfile)
	if err != nil {
		log.Fatalf("testfile: %s\n", err)
		os.Exit(1)
	}
	defer fh.Close()
	fh.Write(rec)
}

func OpenTestFile(name string) *os.File {
	f, err := os.Open(tfile)
    if f == nil {
        fmt.Printf(fmt.Sprintf("can't open file; err=%v\n", err))
        os.Exit(1)
    }		
	if err != nil {
		log.Fatalf("Error opening %s\n", tfile)
		os.Exit(1)
	}
	return f
}

func TestChunkEnd(t *testing.T) {
	f := OpenTestFile(tfile)
	defer f.Close()
	offset := ChunkEnd(f, 0)
	if offset != 11 {
		t.Errorf("Expected offset of %d but got %d\n", 11, offset)
	}
}

func TestChunkSize(t *testing.T) {
	howmany := int64(5)  //how many chunks
	f := OpenTestFile(tfile)
	defer f.Close()
	a := SizeChunks(f, howmany) // returns []int with start_pos, chunk_size

	for i, v := range a {
		fmt.Println(i, v)
	}
	if int64(len(a)) != howmany {
		t.Errorf("Expected a len([][]int64)=%d, but received %d\n", howmany, len(a))
	}
}

/*func TestFindString(t *testing.T) {
	results := make(chan []int)
	recsread := 0
	recsmatch := 0
	iterations := 1

	for i := 0; i < iterations; i++ {
		f := OpenTestFile(tfile)
		defer f.Close()
		go FindString(f, 11, 20, "Z", results, 1)
	}

	for i := 0; i < iterations; i++ {
		ar := <- results
		recsread += ar[0]
		recsmatch += ar[1]
	}

	if recsmatch != 2 {
		t.Errorf("Expected cumulative finds to equal %d, but received %d\n", 2 * iterations, cum)
	}
}*/