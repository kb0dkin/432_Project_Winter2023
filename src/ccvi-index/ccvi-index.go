package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"time"

	"cloud.google.com/go/cloudsqlconn"
	"cloud.google.com/go/cloudsqlconn/postgres/pgxv4"
	"github.com/SebastiaanKlippert/go-soda"
	_ "github.com/lib/pq"
)

//https://data.cityofchicago.org/resource/wrvz-psew.json?$where=trip_miles > 0.1

//import API TOKEN

//create a struct to hold the data

type Trip []struct {
	GeographyType      string `json:"geography_type"`
	CommunityAreaOrZip string `json:"comm_area_or_zip"`
	CommunityAreaName  string `json:"community_area_name"`
	CCVIScore          string `json:"ccvi_score"`
	CCVICategory       string `json:"ccvi_category"`
}

func CSVSample(data_set string) Trip {
	APP_TOKEN := "8nxBA5pgg7aPQ4fDbf4wj8BfM"
	url_format := fmt.Sprintf("https://data.cityofchicago.org/resource/%s", data_set)
	sodareq := soda.NewGetRequest(url_format, APP_TOKEN)
	sodareq.Format = "json"
	
	sodareq.Query.Limit = 1000

	// Gets the response
	//wait 1 second
	time.Sleep(1 * time.Second)
	resp, err := sodareq.Get()
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	// Decodes the response
	var trips Trip
	err = json.NewDecoder(resp.Body).Decode(&trips)
	if err != nil {
		log.Fatal(err)
	}

	return trips

}

func connect(connStr string) *sql.DB {
	cleanup, err := pgxv4.RegisterDriver("cloudsql-postgres", cloudsqlconn.WithIAMAuthN())

	if err != nil {
		log.Fatal(err)
	}

	defer cleanup()

	db, err := sql.Open(
		"cloudsql-postgres",
		connStr)
	if err != nil {
		log.Fatal(err)
	}

	return db
}

func main() {
	// Get today's date
	//02/01/2023 12:00:00 AM
	//https://data.cityofchicago.org/api/id/wrvz-psew.json?$query=select *, :id order by `trip_start_timestamp` asc limit 100
	//Get everything after 2023-01-01

	

	// Get a sample of taxi trips from the Socrata API from today
	trips := CSVSample("xhc6-88s9")

	host := os.Getenv("PGHOST")
	port := os.Getenv("PGPORT")
	user := os.Getenv("PGUSER")
	password := os.Getenv("PGPASS")
	dbname := "bronze"
	connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable", host, port, user, password, dbname)

	db := connect(connStr) // connect to the database

	stmt, err := db.Prepare(`INSERT INTO ccvi_index (geography_type, comm_area_or_zip, community_area_name, ccvi_score, ccvi_category) VALUES ($1, $2, $3, $4, $5) ON CONFLICT (comm_area_or_zip) DO NOTHING`)
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()

	// Insert each taxi trip into the 'taxi_trips' table using a prepared statement
	for _, trip := range trips {
		fmt.Println(trip.GeographyType, trip.CommunityAreaOrZip, trip.CommunityAreaName, trip.CCVIScore, trip.CCVICategory)
		count := 0
		if trip.GeographyType != "" && trip.CommunityAreaOrZip != "" && trip.CommunityAreaName != "" && trip.CCVIScore != "" && trip.CCVICategory != "" {
			_, err = stmt.Exec(
				trip.GeographyType,
				trip.CommunityAreaOrZip,
				trip.CommunityAreaName,
				trip.CCVIScore,
				trip.CCVICategory,
			)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Printf("Inserted community area or zip with ID %s\n", trip.CommunityAreaOrZip)
			fmt.Printf("Count %d\n", count)
			count++
		}
	}

}
