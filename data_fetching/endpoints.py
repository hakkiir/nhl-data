endpoints = {
    "dev": 
        {
            "franchise"         : "http://localhost:8080/api/franchise.json",
            "schedule"          : "http://localhost:8080/api/schedule.json",
            "teams"             : "http://localhost:8080/api/teams.json",
            "roster"            : "http://localhost:8080/api/roster.json",
        },
    "prd":
        {
            "franchise"         : "https://api.nhle.com/stats/rest/en/franchise",
            "schedule"          : "https://api-web.nhle.com/v1/schedule/now",
            "teams"             : "https://api.nhle.com/stats/rest/en/team",
            "roster"            : "https://api-web.nhle.com/v1/roster/<team_tricode>/current",
        }
    }