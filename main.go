package main

import (
	"fmt"
	"os"

	cmdline "github.com/acladenb5/gocmdline"
)

var (
	// Version is the software version, set at compile time
	Version string
	// Build is the build number, set at compile time
	Build string
)

func main() {
	cmdline := cmdline.New()
	cmdline.AddFlag("d", "debug", "Enable debug messages")
	cmdline.AddOption("p", "project", "project_id", "Project to get metrics from")
	cmdline.Parse(os.Args)

	fmt.Println(os.Args[0] + " " + Version + " - " + Build[0:9])
}
