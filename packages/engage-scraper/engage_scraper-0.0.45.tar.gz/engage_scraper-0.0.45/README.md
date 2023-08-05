# Engage Scraper

## Installation

`pip i engage-scraper`

## About

The Engage Scraper is a standalone library that can be included in any service. The purpose of the scraper is to catalog a municipality's council meeting agendas in a usable format for such things as the [engage-client](https://github.com/hackla-engage/engage-client) and [engage-backend](https://github.com/hackla-engage/engage-backend).

To extend this library for your municipality, override the methods of the base class from the `scraper_core/` directory and put it in `scraper_logics/`, prefacing it with your municipality name. For an example see the Santa Monica, CA example in the `scraper_logics/` directory. The Santa Monica example makes use of `htmlutils.py` because it requires HTML scraping for its sources. Feel free to make PRs with new utilities (for example, PDF scraping, RSS scraping, JSON parsing, etc.). The Santa Monica example also uses SQLAlchemy for its models and that is what is preferred for use in the `dbutils.py`, however you can use anything. ORMs are preferred rather than vanilla psycopg2 or the like.

To use the postgres `dbutils.py` make sure to set these 5 environment variables (check `dev.env` and see docker-compose usage below):

- `POSTGRES_HOST` _optional_ a host or hostname that is resolvable. Defaults to localhost
- `POSTGRES_USER` _required_
- `POSTGRES_PASSWORD` _required_
- `POSTGRES_PORT` _optional_ defaults to 5432
- `POSTGRES_DB` _required_ The database used for cataloging your municipality's agendas.

## An example of using the Santa Monica scraper library

```{python}
from engage_scraper.scraper_logics import santamonica_scraper_logic

scraper = santamonica_scraper_logic.SantaMonicaScraper(committee="Santa Monica City Council")
scraper.get_available_agendas()
scraper.scrape()
```

### For SantaMonicaScraper instantiation

#### For twitter utils used in SantaMonicaScraer

To use the santa monica logic, you must create an App on twitter (will work to make this optional). Following making an app, please use the structure `dev.env` file to insert the appropriate parameters. But make sure not to make changes to the repository's file. Copy the file up one directory and edit it there. Following the edit, use the `docker-compose.yml` for testing. You can add examples to `examples/` and run them from the script in `scripts/` using the docker container.

#### For the SantaMonicaScraper class the init has these options

- `tz_string="America/Los_Angeles"` # defaulted string
- `years=["2019"]` # defaulted array of strings of years
- `committee="Santa Monica City Council"` # defaulted string of council name

### The exposed API methods for scraper are

- `.get_available_agendas()` # To get available agendas, no arguments
- `.scrape()` # To process agendas and store contents

### Feel free to expose more

- Write wrappers for internal functions if you want to expose them
- Write extra functions to handle more complex municipality-specific tasks
