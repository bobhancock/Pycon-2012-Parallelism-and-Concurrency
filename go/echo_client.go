package main

import (
	"log"
	"net"
	"fmt"
	"bufio"
	"sync"
	"os"
	"runtime"
	"strconv"
	"time"
	"stats"
)

// Divisor to convert nanoseconds to seconds
//const MS_DIVISOR = 1000000000.0

var times []int64
var errors []string

func main() {
	// prog maxprocs host connections reps
	if len(os.Args) < 5 {
		fmt.Println("maxproc targehost conns reps")
		return 
	}
	max_procs, err := strconv.Atoi(os.Args[1])
	if err != nil {
		log.Fatalf("maxprocs conversion", err)
		panic(err)
	}
	if max_procs > 4 {
		max_procs = 4
	}
	runtime.GOMAXPROCS(max_procs)

	// target host
	host := os.Args[2]

	// number of connections
	max_connections, err := strconv.Atoi(os.Args[3])
	if err != nil {
		log.Fatalf("Max connections", err)
		panic(err)
	}
	// reptitions for each connections
	reps, err := strconv.Atoi(os.Args[4])
	if err != nil {
		log.Fatalf("reps conversion", err)
		panic(err)
	}
	packet_size := 2048
	
	line := ""
	for i := 0; i < packet_size; i++ {
		line += "Z"
	}
	line += "\n"

	// Open connections to host
	var conns []net.Conn
	thost := host+":2020"
	for i := 0; i < max_connections; i++ {
		c, err := net.Dial("tcp", thost)
		if err != nil {
			log.Fatalf("dial error: %v", err)
			panic(err)		
		}
		defer c.Close()
		conns = append(conns, c)
		//fmt.Printf("Connection %d\n", i)
	}
	//fmt.Printf("Opened %d connections\n", max_connections)

	count := 0
	wg := new(sync.WaitGroup)
	wg.Add(max_connections)

	// Launch a go routine for each connection and perform
	for _, con := range conns {
		go echo(con, line, count, wg, reps)
		count += 1
	}
	//fmt.Printf("Launched %d goroutines.\n", count)
	wg.Wait()
	for _,v := range errors {
		fmt.Println(v)
	}

	min := float64(min64(times)) * 1e-9
	max :=  float64(max64(times)) * 1e-9
	mean :=  float64(sum64(times)) / float64(len(times)) * 1e-9 

	var ftimes []float64
	for _, tv := range times {
//		fmt.Printf("%d %f\n", tv, float64(tv))
		ftimes = append(ftimes, float64(tv))
	}
	stddev := stats.StatsSampleStandardDeviation(ftimes) * 1e-9
	
	//for j := 0; j < len(times); j++ {
	//	fmt.Println(times[j])
	//}
	fmt.Printf("%d,%d,%f,%f,%f,%f\n", max_connections, reps, min, max, mean, stddev)
}
 
func echo(con net.Conn, line string, id int, wg *sync.WaitGroup, reps int ) {
	for i := 0; i < reps; i++ {
		a := time.Nanoseconds()
		_, err := con.Write([]byte(line))
		if err != nil {
			szw := fmt.Sprintf("Conn=%d-%d: Write error: %v\n", id, i, err)
			errors = append(errors, szw)
			fmt.Println(szw)
			wg.Done()
			return
		}

		bufr := bufio.NewReader(con)
		_, err = bufr.ReadString('\n')
		/* If you need to assure yourself that the correct number of echo responses
		 are being received, replace the above line with this section and on the 
		 command line  go-echo-client 1 192.168.1.2 1000 2|grep xyz|wc -l
		 and you should see 2000 (1000 connections X 2 repitions).
		s, err := bufr.ReadString('\n')
		if s == line {
			fmt.Println("xyz")
		}
		*/

		if err != nil {
			szr :=fmt.Sprintf("Conn=%d-%d: Read error: %v\n", id, i, err)
			errors = append(errors, szr)
			fmt.Println(szr)
//			log.Fatalf("Conn=%d: Read error: %v", id, err)
//			panic(err)
			wg.Done()
			return
		}
		times = append(times, (time.Nanoseconds() - a))
	}
	//fmt.Printf("%d: echoed reps=%d\n", id, reps)
	wg.Done()
}

// Sum of an array of int64
func sum64(data []int64) (sum int64) {
	for _, v := range data {
		sum += v
	}
	return
}

// Max value in a slice of 
func max64(a []int64) int64 {
	m := a[0]
	for i := 1; i < len(a); i++ {
		if a[i] > m {
			m = a[i]
		}
	}
	return m	
}

// Min value in a slice of 
func min64(data []int64) int64 {
	min := data[0]
	for _, v := range data {
		if v < min {
			min = v
		}
	}
	return min
}
