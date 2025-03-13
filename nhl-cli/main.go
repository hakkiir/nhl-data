/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
*/
package main

import (
	"fmt"
	"os"

	"github.com/hakkiir/nhl-data/nhl-cli/cmd"
	data "github.com/hakkiir/nhl-data/nhl-cli/internal/database"
)

func main() {

	db := new(data.Database)

	err := db.OpenDatabase()
	if err != nil {
		fmt.Println("db connection failed, shutting down")
		os.Exit(1)
	}
	cmd.RootCmd.AddCommand(cmd.NewGetStandingsCmd(db))
	defer db.Close()
	cmd.Execute()
}
