package main

import (
	"bigfile"
	"fmt"
	"log"
	"os"
	"strings"
)

// Read the big file and search for Target_Username in each record.
// If found write out to a file in the tmp directory.
// It takes the parameters from settings.py which is specified
// with a canonical path on the command line.
func main() {
	if len(os.Args) < 2 {
		log.Println("usage: bigfile_brute settings_file")
		return 
	}
	sfile := os.Args[1]
	sfile = strings.Trim(sfile, "\" ")
	q := bigfile.Settings(sfile, "TARGET_USERNAME")
	q = strings.Trim(q, "\"")
//	fmt.Printf("1=%s\n",q)

	bf := bigfile.Settings(sfile, "BIG_FILE")
	bf = strings.Trim(bf, "\" ")
	//fmt.Printf("bigfile=%s\n", bf)

	fmt.Println( bigfile.Brute(bf, q))
//	fmt.Printf("%d,%d\n", r, m)
}