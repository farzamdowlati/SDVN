#!/bin/bash
# IEEE Xplore metadata fetcher — CONSERVATIVE: check key status, fetch 2 abstracts
# Rate discipline: 10 req/s limit is per-second; 200/day is the real budget.
# Run only during ET business hours once key shows ACTIVE (not "Developer Inactive").
KEY="$(grep '^IEEE_API_KEY=' "$HOME/.hermes/.env" | cut -d= -f2- | tr -d '"')"
fetch() { # $1=doi $2=outfile
  curl -s --max-time 30 "http://ieeexploreapi.ieee.org/api/v1/search/articles?apikey=$KEY&format=json&max_records=1&doi=$1" -o "$2" -w "http:%{http_code} "
  head -c 120 "$2"; echo
}
case "${1:-}" in
  status)
    fetch "10.1109/ACCESS.2024.3459952" /tmp/ieee_probe.json
    ;;
  papers)
    # Hechmi 2024 (ComNet conference) + Liu 2023 (ACM — NOTE: ACM DOI won't resolve on IEEE API; kept for the record)
    fetch "10.1109/ComNet64071.2024.10987235" /tmp/ieee_hechmi.json
    sleep 2
    fetch "10.1145/3600061.3603124" /tmp/ieee_liu.json
    ;;
  *) echo "usage: ieee_fetch.sh status|papers" ;;
esac
