# webbscrapers_api
Python module to access Webbscrapers API - https://webbscrapers.live

Created for easy access to Webbscrapers API - an API that allows for easy access to World Health Organisation reports - parsed and scanned by symptoms, location, diseases, etc.

Created for UNSW's SENG3011 course.

# Documentation

## Register

First, register a user to get the authorization token. You need the authorization token to access /reports, /statistics, and /covid-19 endpoints. You must supply an email and password.

```
import webbscrapers_api

webbscrapers_api.register("test@test.com", "this_is_my_password")

```

## Login
If you have lost the authorization token, you can login and get the token again.

```
import webbscrapers_api

webbscrapers_api.login("test@test.com", "this_is_my_password")
```

## Reports

To get reports from the World Health Organisation, use getReports()

```
import webbscrapers_api
from datetime import datetime

# webbscrapers_api.getReports(authorization_token, startDateTime, endDateTime, keyTerms, location, timezone)
webbscrapers_api.getReports("my_authorization_token", datetime(2019, 1, 1, 0, 0, 0), datetime(2020, 1, 1, 0, 0, 0), ['coronavirus', 'hiv'], 'Sydney', 'Australia/Sydney')
```

## Covid-19 Cases

To get the current covid-19 cases by country/state/territory, use getCovid19Cases()

```
import webbscrapers_api

webbscrapers_api.getCovid19Cases("my_authorization_token")
```

## Statistics

To get server statistics, use getStatistics()

```
import webbscrapers_api

webbscrapers_api.getStatistics("my_authorization_token")
```
