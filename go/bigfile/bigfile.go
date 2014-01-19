// Package to provide functions for processing the "bigfile" used
// for the Parallelism and Concurrency presentation.
package bigfile

import (
	"fmt"
	"io"
	"os"
	"bufio"
	"strings"
	"log"
	"regexp"
)

// Targetusername returns the value 
// for the key (k) in  the 
// settings.py file specified by the 
// argument s.
func Settings(s, k string) string {
	fp, err := os.Open(s)
	if err != nil {
		fmt.Printf("Could not open file %s.", s)
		panic(err)
	}
	defer fp.Close()
	r := bufio.NewReader(fp)

	for {
		line, isp, err := r.ReadLine()
		if err != nil {
			fmt.Print("Error reading file. Stderr=%s.  err=%d",os.Stderr, err)
            break
		}
		if isp {
            fmt.Fprintln(os.Stderr, "Line too long")
            break
        }
		l := string(line)
		if strings.HasPrefix(l, "#") {
			continue
		}
		if strings.Contains(l, k) {
			el := strings.Split(l, " ")
			return el[2]
		}
	}
	return ""
}

// Bigfilebrute reads a file, searchs for a string
// in each record.
// Returns the number of records read and matched.
//func Brute(in,  query string) (int, int) {
func Brute(in,  query string) int {
	fin, err := os.Open(in)
	if err != nil {
		fmt.Printf("Could not open file %s.", in)
		panic(err)
	}
	defer fin.Close()

//	fi, err := os.Stat(in)
	if err != nil{
		fmt.Printf("Could not stat %s\n", in)
		panic(err)
	}

//	size :=  int(fi.Blksize)
	r := bufio.NewReader(fin)
	//recsread := 0
	recsmatch := 0
	for {
		line, isp, err := r.ReadLine()
		if err != nil {
			if err == io.EOF {
				break
			} else {
				fmt.Printf("Error reading file. Stderr=%s.  err=%d",os.Stderr, err)
				break
			}
		}
		if isp {
            fmt.Fprintln(os.Stderr, "Line too long")
            break
        }
		l := string(line)
		if strings.Contains(l, "ssbrtg") {
			//fmt.Println(l)
			//w.WriteString(l+"\n")
			recsmatch++
		}
        //recsread++
	}
	//return recsread, recsmatch
	return recsmatch
}

// Chunks breaks a file into n chunks.  Each chunk
// searches for key in a record.  
// Will suffixarray make the record search logrithmic?
//func Chunks(in, key string, n int) (int, int) {
func Chunks(in, key string, n int) int {
	fin, err := os.Open(in)
	if err != nil {
		fmt.Printf("Could not open file %s.", in)
		panic(err)
	}
	defer fin.Close()

//	recsread := 0
	recsmatch := 0

	//fmt.Printf("Chunks: in=%s\n", in)
	fi, err := os.Stat(in)
	if err != nil{
		fmt.Printf("Could not stat %s\n", in)
		panic(err)
	}

	chunksize := fi.Size() / int64(n)
	fmt.Printf("Chunks: chunksize=%d\n", chunksize)

//	return recsread,recsmatch
	return recsmatch
}

// ChunkEnd starts from the end of the chunk and increments 
// until it finds a newline and returns that position.
// If it encounters EOF before a new line, it returns -1.
func ChunkEnd(f *os.File, start int64) int64 {
	nl := byte('\n')
	buf := make([]byte, 1)
	curpos := start
	fmt.Println("ChunkeEnd start=",start)

	readseek := io.ReadSeeker(f)
	offset, err := readseek.Seek(start, 0)
	if err != nil {
		log.Fatalf(fmt.Sprintf("FindString: error on seek-%n\n", err))
		os.Exit(1)
	}
	if offset != start {
		log.Fatalf("Expected offset of %d and received %d\n", start, offset)
	}
	reader := io.ReaderAt(f)

	for {
		nr, _ := reader.ReadAt(buf, curpos)
		//fmt.Printf("curpos=%d nr=%d buf=%s\n", curpos, nr, buf)
		curpos++
		if nr == 0 || buf[0] == nl { // EOF or neline
			break
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

	fsize := fstat.Size()
	fmt.Printf("fsize=%d\n",fsize)
	chunk_size = fsize/howmany
	fmt.Printf("chunk_block=%d\n", chunk_size)

	start :=  int64(0)
	var end, size int64

	for i := int64(0); i < howmany; i++ {
		if start + chunk_size < fsize {
			end = ChunkEnd(f, start + chunk_size)
			size = end - start
		} else {
			end = fsize
			size = end - start
			fmt.Printf("end=%d start=%d\n", end, start)
		}
		fmt.Printf("i=%d end=%d start=%d chunk_size=%d\n", i, end, start, chunk_size)
		chunks = append(chunks, []int64{start, size})
		start = end + 1
		fmt.Println("After +1: start=",start)
	}
	fmt.Println("chunks=",chunks)
	return chunks
}
 
// FindString reads lines in a chunk of a file from start to start+chunksize
// and searches for the query string.  Number of matches are sent to the
// done channel
// TODO: returns too man records read and found.
func FindString(f *os.File, start, chunksize int64, query string, done chan []int, name int) {
	//fmt.Println("name: start, chunksize", name, start, chunksize)
	recsread := 0
	recsmatch := 0 
	var l string
	
	readseek := io.ReadSeeker(f)
	offset, err := readseek.Seek(start, 0)
	if err != nil {
		log.Fatalf(fmt.Sprintf("FindString: error on seek-%v\n", err))
		os.Exit(1)
	}
	if offset != start {
		log.Fatalf("Expected offset of %d and received %d\n", start, offset)
	}

	reader := bufio.NewReader(readseek)
	fmt.Printf("FindString: name=%d start=%d, chunksize=%d, query=%s, offset=%d\n",
		name,start,chunksize,query,offset)

	bytes_read := int64(0)

	for  bytes_read < chunksize {
		line, isp, err := reader.ReadLine()
		if err != nil {
			if err == io.EOF {
				break
			} else {
				log.Print(fmt.Sprintf("Error reading file.  err=%v\ns", err))
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
		//fmt.Printf("name: %d line=%s\n",name, l)

		if strings.HasPrefix(l, "#") {
			continue
		}

		match, err := regexp.MatchString(query, l)
		if err != nil {
			log.Printf(fmt.Sprintf("FindString: regexp.MatchString-%v\n", err))
			continue
		}
		if match == true {
			//fmt.Printf("MATCH name: %d line=%s\n\n",name, l)
			//TODO: split line and write rec number to stdout to 
			//see which recs are duplicates
			recsmatch += 1
			s := strings.Split(string(line), " ")
			fmt.Printf("linenum:%s\n",s[0])
		}
	}
	recs := []int{recsread, recsmatch}
	done <- recs
}