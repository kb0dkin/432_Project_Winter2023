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

	// Create a new file with the name results.csv
	file, err := os.Create("results.csv")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	// Create a new CSV writer that writes to the file
	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Create a new CSV reader that reads from the response body
	reader := csv.NewReader(resp.Body)

	// Loop through the records and write them to the file
	for {
		record, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}
		err = writer.Write(record)
		if err != nil {
			log.Fatal(err)
		}
	}
}

// main

func main() {
	CSVSample("wrvz-psew", "trip_miles > 10")
}