package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"

	cmdline "github.com/acladenb5/gocmdline"
	yaml "gopkg.in/yaml.v2"
)

// Variables
var (
	// Version is the software version, set at compile time
	Version string
	// Build is the build number, set at compile time
	Build string
)

// Structs

// Services structure
type Services struct {
	Services map[string][]string
}

// MetricVal structure
type MetricVal struct {
	Metric      string
	ItemID      string
	ItemName    string
	MetricValue string
}

// RunQuery function
func runQuery(metric string) MetricVal {
	// Time to put some code here
	var metricVal MetricVal
	metricVal.Metric = metric
	metricVal.ItemID = "foo"
	metricVal.ItemName = "bar"
	metricVal.MetricValue = fmt.Sprintf("%f", 2.021)
	return metricVal
}

// Main routine
func main() {
	cmdline := cmdline.New()
	cmdline.AddFlag("v", "version", "Display version and exits")
	cmdline.AddFlag("d", "debug", "Enable debug messages")
	cmdline.AddOption("m", "metrics", "metrics", "File containing the list of available metrics")
	cmdline.AddOption("p", "project", "project", "Project to get metrics from")
	cmdline.AddOption("s", "service", "service", "Service to check")
	cmdline.Parse(os.Args)

	if cmdline.IsOptionSet("v") {
		// fmt.Println(os.Args[0] + " - Version " + " - Build " + Build[0:9])
		log.Println(os.Args[0] + " - Version ")
		os.Exit(0)
	}

	if !cmdline.IsOptionSet("project") {
		log.Fatalln("Project is not set")
	}

	if !cmdline.IsOptionSet("service") {
		log.Fatalln("Service is not set")
	}

	var serviceListFile string
	var projectID = cmdline.OptionValue("project")
	var serviceID = cmdline.OptionValue("service")

	if !cmdline.IsOptionSet("metrics") {
		serviceListFile = "./metrics_list.yaml"
	} else {
		serviceListFile = cmdline.OptionValue("metrics")
	}

	fmt.Println(projectID, serviceID, serviceListFile)

	var services Services

	svcList, errSvcList := ioutil.ReadFile(serviceListFile)

	if errSvcList != nil {
		log.Fatalln(errSvcList)
	}

	erryaml := yaml.Unmarshal(svcList, &services)

	if erryaml != nil {
		log.Fatalln(erryaml)
	}

	for _, metric := range services.Services[serviceID] {
		// fmt.Println(metric)
		mval := runQuery(metric)
		fmt.Println(mval)
		// TODO: call a function that will return the following info:
		// ID: the id of the item in the service
		// Name: the name of the item in the service
		// Value: the value of the metric
	}
}