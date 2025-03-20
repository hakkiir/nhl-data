package data

import (
	"database/sql"
	"fmt"
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"
	_ "github.com/lib/pq"

	"context"
	"text/tabwriter"
	"time"
)

type Database struct {
	DB *sql.DB
}

func (db *Database) OpenDatabase() error {
	err := godotenv.Load("../.env")
	if err != nil {
		log.Fatalf("Error loading .env file: %v", err)
	}
	dbURL := os.Getenv("DB_URL")
	db.DB, err = sql.Open("postgres", dbURL)
	if err != nil {
		return err
	}
	return db.DB.Ping()
}

func (db *Database) Close() {
	if db != nil {
		db.DB.Close()
	}
}

func (db *Database) PrintStandings() {

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	var standings_timestamp time.Time
	err := db.DB.QueryRowContext(ctx, "SELECT max(standings_datetime_local) from current_standings").Scan(&standings_timestamp)
	if err != nil {
		log.Fatalf("Failed to scan row: %v", err)
	}

	// Create a tab writer
	writer := tabwriter.NewWriter(os.Stdout, 0, 0, 5, ' ', tabwriter.AlignRight)

	// Print header
	fmt.Fprintln(writer, "")
	fmt.Fprintln(writer, "################################################")
	fmt.Fprintf(writer, "NHL standings (updated at %v)\n", standings_timestamp.Format("2006-01-02 15:04:05"))
	fmt.Fprintln(writer, "################################################")
	fmt.Fprintln(writer)

	db.printStandingsByDivision("Central", writer)
	db.printStandingsByDivision("Pacific", writer)
	db.printStandingsByDivision("Metropolitan", writer)
	db.printStandingsByDivision("Atlantic", writer)

	writer.Flush()
}

func (db *Database) printStandingsByDivision(division_name string, writer *tabwriter.Writer) {

	divison := fmt.Sprintf("~%s Division~", division_name)
	tilde := strings.Repeat("~", len(divison))

	fmt.Fprintf(writer, "\t%s\n", tilde)
	fmt.Fprintf(writer, "\t%s\n", divison)
	fmt.Fprintf(writer, "\t%s\n", tilde)
	fmt.Fprintln(writer, "Team\tPoints\tGames played\tW\tL\tOT\tL10\t")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	query := `SELECT t.team_name, cs.points, cs.games_played, cs.wins, cs.losses, cs.ot_losses, cs.l10_wins, cs.l10_losses, cs.l10_ot_losses
			from current_standings cs 
			join divisions d on cs.division_id = d.division_id 
			join teams t on cs.team_id = t.team_id 
			where
			d.division_name = $1
			`
	rows, err := db.DB.QueryContext(ctx, query, division_name)
	if err != nil {
		log.Fatalf("query failed: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var team_name string
		var points int
		var games_playes int
		var wins int
		var losses int
		var ot_losses int
		var l10wins int
		var l10losses int
		var l10otlosses int

		err = rows.Scan(&team_name, &points, &games_playes, &wins, &losses, &ot_losses, &l10wins, &l10losses, &l10otlosses)
		if err != nil {
			log.Fatalf("Failed to scan row: %v", err)
		}
		// Print row data
		fmt.Fprintf(writer, "%s\t%d\t%d\t%d\t%d\t%d\t%s\t\n", team_name, points, games_playes, wins, losses, ot_losses, fmt.Sprintf("%d-%d-%d", l10wins, l10losses, l10otlosses))
	}

	// Check for row iteration errors
	if err := rows.Err(); err != nil {
		log.Fatalf("Error iterating rows: %v", err)
	}
	fmt.Fprintln(writer)
}
