import os
platform = os.getenv("PLATFORM")

if platform == "dev":
    # static-data
    FRANCHISE_URL = "http://localhost:8080/api/franchise.json"
    
    # dynamic-data
    SCHEDULE_URL = "http://localhost:8080/api/schedule.json"

else:
    # static
    FRANCHISE_URL = "https://api.nhle.com/stats/rest/en/franchise"
    
    # dynamic
    SCHEDULE_URL =  "ttps://api-web.nhle.com/v1/schedule/now"