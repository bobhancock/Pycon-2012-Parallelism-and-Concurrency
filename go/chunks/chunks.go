package chunks

import (
	"fmt"
	"os"
	"io"
	"bufio"
	"strings"
	"log"
	"regexp"
)

// ChunkEnd starts from the end of the chunk and increments 
// until it finds a newline and returns that position.
// If it encounters EOF before a new line, it returns -1.
func ChunkEnd(f *os.File, start int64) int64 {
	nl := byte('\n')
	buf := make([]byte, 1)
	curpos := start

	readseek := io.ReadSeeker(f)
	offset, err := readseek.Seek(start, 0)
	if err != nil {
		log.Fatalf("FindString: error on seek-%n", err.String())
		os.Exit(1)
	}
	if offset != start {
		log.Fatalf("Expected offset of %d and received %d\n", start, offset)
	}
	reader := io.ReaderAt(f)

	for {
		nr, _ := reader.ReadAt(buf, curpos)
		if nr == 0 { // EOF
			break
		}
		if buf[0] == nl {
			break
		} else {
			 curpos++
		}
	}
	return int64(curpos)
} 

// SizeChunks divides a file into howmany chunks and
// returns a slice of slices of two members that contain the start of the chunk
// and the size of the chunk.
// a[0] = [0, 230]
// a[1] = [231 230]
 // a[3] = [232, 20]  <-- chunk before EOF
func SizeChunks(f *os.File,howmany int64) [][]int64 {
	chunks := [][]int64{}

	fstat, err := f.Stat()
	if err != nil {
		panic(err)
	}
	var chunk_size int64

	fsize := fstat.Size
	fmt.Printf("fsize=%d\n",fsize)
	chunk_size = fsize/howmany
	fmt.Printf("chunk_block=%d\n", chunk_size)

	chunk_start := int64(0)
	chunk_end := int64(0)

	for i := int64(0); i < howmany - 1; i++ {
		if chunk_start + chunk_size < fsize {
			chunk_end = ChunkEnd(f, chunk_start + chunk_size)
			chunk_size = chunk_end - chunk_start
		} else {
			chunk_end = fsize
			chunk_size = fsize - chunk_start
		}
		chunks = append(chunks, []int64{chunk_start, chunk_size})
		chunk_start = chunk_end + 1
	}
	return chunks
}
 
// FindString reads lines in a chunk of a file from start to start+chunksize
// and searches for the query string.  Number of matches are sent to the
// done channe
func FindString(f *os.File, start, chunksize int64, query string, done chan []int, name int) {
	//fmt.Println("name: start, chunksize", name, start, chunksize)
	recsread := 0
	recsmatch := 0 
	var l string
	
	readseek := io.ReadSeeker(f)
	offset, err := readseek.Seek(start, 0)
	if err != nil {
		log.Fatalf("FindString: error on seek-%n", err.String())
		os.Exit(1)
	}
	if offset != start {
		log.Fatalf("Expected offset of %d and received %d\n", start, offset)
	}

	reader := bufio.NewReader(readseek)
	fmt.Printf("FindString: name=%d start=%d, chunksize=%d, query=%s, offset=%d\n",
		name,start,chunksize,query,offset)

	bytes_read := int64(0)

	for {
		if bytes_read >= chunksize {
			break
		}
		line, isp, err := reader.ReadLine()

		if err != nil {
			if err == os.EOF {
				break
			} else {
				log.Print("Error reading file.  err=%s", err.String())
				break
			}
		}
		if isp {
			log.Printf("FindString: Line too long")
			break
		}
		bytes_read += int64(len(line))
		
		l = string(line)
		recsread += 1
		fmt.Printf("name: %d line=%s\n",name, l)

		if strings.HasPrefix(l, "#") {
			continue
		}

		match, err := regexp.MatchString(query, l)
		if err != nil {
			log.Printf("FindString: regexp.MatchString-%s\n", err.String())
			continue
		}
		if match == true {
			//fmt.Printf("MATCH name: %d line=%s\n\n",name, l)
			recsmatch += 1
		}
	}
	recs := []int{recsread, recsmatch}
	done <- recs
}