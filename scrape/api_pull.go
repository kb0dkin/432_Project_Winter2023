package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/SebastiaanKlippert/go-soda"
)

//https://data.cityofchicago.org/resource/wrvz-psew.json?$where=trip_miles > 0.1

//import API TOKEN




func CSVSample(data_set string, query string) {
	APP_TOKEN := os.Getenv("APP_TOKEN")
	url_format := fmt.Sprintf("https://data.cityofchicago.org/resource/%s", data_set)
	sodareq := soda.NewGetRequest(url_format, APP_TOKEN)
	sodareq.Format = "csv"
	sodareq.Query.Where = query
	sodareq.Query.Limit = 10

	resp, err := sodareq.Get()
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	//print the response
	reader := csv.NewReader(resp.Body)
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(record)
	}


}

// main

func main() {
	CSVSample("wrvz-psew", "trip_miles > 10")
}