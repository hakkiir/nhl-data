/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	data "github.com/hakkiir/nhl-data/nhl-cli/internal/database"
	"github.com/spf13/cobra"
)

// standingsCmd represents the standings command
func NewGetStandingsCmd(db *data.Database) *cobra.Command {
	return &cobra.Command{
		Use:   "standings",
		Short: "A brief description of your command",
		Long: `A longer description that spans multiple lines and likely contains examples
			and usage of using your command. For example:

			Cobra is a CLI library for Go that empowers applications.
			This application is a tool to generate the needed files
			to quickly create a Cobra application.`,
		Run: func(cmd *cobra.Command, args []string) {
			db.PrintStandings()
		},
	}
}
