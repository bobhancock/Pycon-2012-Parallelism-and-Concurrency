package main

import (
    "bufio"
    "log"
    "net"
	"strconv"
	"os"
	"fmt"
	"runtime"
	//"time"
	//"stats"
	"strings"
)

var times []int64
var errors []string

func main() {
	if len(os.Args) < 3 {
		fmt.Println("usage: echo_server gomaxprocs port")
		return
	}
	// Number of GOMAXPROCS
	max_procs, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Printf("Atoi: %d", err)
		return
	}
	if max_procs > 4 {
		max_procs = 4
	}
	runtime.GOMAXPROCS(max_procs)

    port := ":" + os.Args[2]
    // ln, err := net.Listen("tcp", ":2020")
    ln, err := net.Listen("tcp", port)
    if err != nil {
        log.Fatalf("listen error: %v", err)
    }
    accepted := 0
    for {   
        conn, err := ln.Accept()
        if err != nil {
            log.Fatalf("accept error: %v", err)
        }
        accepted++
        go serve(conn)

		/*for {
		a := time.Seconds()
		var ftimes []float64
			for _, tv := range times {
				//		fmt.Printf("%d %f\n", tv, float64(tv))
				ftimes = append(ftimes, float64(tv))
			}
			fmt.Printf("Max: %f\n", stats.StatsMax(ftimes) * 1e-9)
			fmt.Printf("Min: %f\n", stats.StatsMin(ftimes) * 1e-9)
			fmt.Printf("Std: %f\n", stats.StatsSampleStandardDeviation(ftimes) * 1e-9)
		}*/
        //log.Printf("Accepted %d", accepted)
    }
}

func serve(conn net.Conn) {
    bufr := bufio.NewReader(conn)
	
    for { 
		//a := time.Nanoseconds()

        line, err := bufr.ReadString('\n')
        if err != nil {
            return
        }
		if line == "" {
			return
		}

		if strings.HasPrefix(line, "quit") {
			conn.Write([]byte("ACK\n"))
		} else {
			conn.Write([]byte(line))
            fmt.Println(line)
		}
	//	times = append(times, time.Nanoseconds() - a)
    }
}
