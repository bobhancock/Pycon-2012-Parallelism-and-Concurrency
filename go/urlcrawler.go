package main

import (
	"fmt"
	"net/http"
	"os"
	"io/ioutil"
	"strconv"
	"time"
	"runtime"
)

var urls = []string{"http://www.python.org",
	"http://www.ibm.com",
	"http://google.com",
	"http://www.bbc.co.uk/",
	"http://www.json.org/",
	"http://www.lemonde.fr/",
	"http://yahoo.com",
	"http://www.amazon.com",
	"http://www.cnn.com",
	"http://www.nytimes.com",
	"http://www.bradmehldau.com",
	"http://bobhancock.org",
	"http://eventlet.net/doc/design_patterns.html",
	"http://golang.org/doc/effective_go.html",
	"http://docs.sun.com/source/816-6698-10/replicat.html",
	"http://rss.cnn.com/rss/cnn_world.rss",
	"http://rss.cnn.com/rss/cnn_us.rss",
	"http://rss.cnn.com/rss/si_topstories.rss",
	"http://rss.cnn.com/rss/money_latest.rss",
	"http://rss.cnn.com/rss/cnn_allpolitics.rss",
	"http://rss.cnn.com/rss/cnn_crime.rss",
	"http://rss.cnn.com/rss/cnn_tech.rss",
	"http://rss.cnn.com/rss/cnn_space.rss",
	"http://rss.cnn.com/rss/cnn_health.rss",
	"http://rss.cnn.com/rss/cnn_showbiz.rss",
	"http://rss.cnn.com/rss/cnn_travel.rss",
	"http://rss.cnn.com/rss/cnn_living.rss",
	"http://rss.cnn.com/rss/cnn_freevideo.rss",
	"http://rss.cnn.com/rss/cnn_mostpopular.rss",
	"http://rss.cnn.com/rss/cnn_latest.rss",
	"http://www.nytimes.com/services/xml/rss/nyt/Business.xml",
	"http://finance.yahoo.com/rss/headline?s=mhp",
	"http://www.ft.com/servicestools/newstracking/rss#world",
	"http://finance.yahoo.com/rss/headline?s=mhp",
	"http://golang.org"}

const MS_DIVISOR = 1000000000.

type request struct {
	url    string
	replyc chan string
}

type opGet func(url string) string

func startServer(op opGet, procLimit int) (service chan *request, quit chan bool) {
	service = make(chan *request, procLimit) //Dow we need to buffer the service channel
	var sem = make(chan int, procLimit+1)
	quit = make(chan bool)
	go server(op, service, sem, quit)
	return service, quit
}

func server(op opGet, service chan *request, sem chan int, quit chan bool) {
	for {
		select {
		case req := <-service:
			//You can use the sem channel as a sempahore to limit the number
			//of simultaneous processes.  Set the buffer size on sem to the 
			//number of processes you want, and the blocking of this channel
			//will limit the invocations.
			sem <- 1
			go process(op, req)
			<-sem
		case <-quit:
			return
		}
	}
}

func process(op opGet, req *request) {
	//start_process := time.Nanoseconds()
	//fmt.Printf("%s,process start,%d\n",req.url,start_process)
	reply := op(req.url)
	//return_op := time.Nanoseconds()
	//fmt.Printf("%s,process opGet,%d\n",req.url, time.Nanoseconds() - start_process)
	req.replyc <- reply
	//fmt.Printf("%s,process <- replyt,%d\n",req.url, time.Nanoseconds() - return_op)
	//fmt.Printf("%s,process all opGet,%d\n", req.url, time.Nanoseconds() - start_process)
}

// Return the contents of a URL 
func getURL(url string) string {
	var d time.Duration
	start := d.Nanoseconds()
	//var b[]byte
	r, err := http.Get(url)
	if err != nil {
		fmt.Printf("\n---> Get()-Error: %s\n\n", err)
		os.Exit(1)
	}
	//b, _ = ioutil.ReadAll(r.Body);
	_, _ = ioutil.ReadAll(r.Body)
	r.Body.Close()

	nsecs := (d.Nanoseconds() - start)
	//r_time := float64(nsecs) / MS_DIVISOR
	//return fmt.Sprintf("%s|%d|%f",url,len(string(b)),r_time)
	//return fmt.Sprintf("%s,%d,%d",url,len(string(b)),nsecs)
	return fmt.Sprintf("%s,opGet,%d", url, nsecs)
}

func main() {
	procLimit, err := strconv.Atoi(os.Args[1])
	if err != nil {
		fmt.Printf("Atoi: %d", err)
		return
	}
	if procLimit < 1 {
		procLimit = len(urls)
	}

	runtime.GOMAXPROCS(1)
	const iterations = 10
	n := len(urls)
	service, quit := startServer(getURL, procLimit)
	var d time.Duration

	for i := 0; i < iterations; i++ {
		reqs := make([]request, len(urls))

		start_inside_loop := d.Nanoseconds()
		for i := 0; i < n; i++ {
			req := &reqs[i]
			req.url = urls[i]
			req.replyc = make(chan string, 1024)
			service <- req
		}
		for i := n - 1; i >= 0; i-- { // doesn't matter what order
			fmt.Println(<-reqs[i].replyc)
		}
		fmt.Printf("Inside_loop,%d\n", d.Nanoseconds()-start_inside_loop)
	}
	quit <- true //Shutdown server
	fmt.Printf("urls:%d\n", n)
	fmt.Printf("Server processes: %d\n", procLimit)
}
