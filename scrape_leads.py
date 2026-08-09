#!/usr/bin/env python3
"""Find US contractor businesses with no listed website, via the official
Google Places API (Text Search + Place Details).

Deliberately does NOT attempt to find/guess decision-maker names or emails
- those aren't public Places data. See README.md for why, and for
compliant ways to fill those columns in yourself.

Usage:
    python3 scrape_leads.py --trade "general contractor" --target 100 --output leads.csv
"""
import argparse
import csv
import os
import random
import sys
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

from us_cities import US_CITIES

TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
DETAILS_FIELDS = (
    "name,formatted_phone_number,international_phone_number,website,"
    "formatted_address,url,business_status,rating,user_ratings_total"
)

SOCIAL_DOMAINS = (
    "facebook.com", "instagram.com", "yelp.com", "houzz.com",
    "linkedin.com", "twitter.com", "x.com", "nextdoor.com",
)

CSV_FIELDS = [
    "business_name", "formatted_phone", "international_phone", "address",
    "city", "state", "google_maps_url", "rating", "review_count",
    "place_id", "decision_maker_name", "decision_maker_role", "email",
    "notes", "source_query", "retrieved_at",
]


def load_api_key():
    load_dotenv()
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        sys.exit(
            "GOOGLE_PLACES_API_KEY not set. Copy .env.example to .env and "
            "fill in a Places API key (see README.md)."
        )
    return key


def text_search(query, api_key, session, sleep_s):
    """Return all results for a Text Search query, following pagination."""
    results = []
    params = {"query": query, "key": api_key}
    while True:
        resp = session.get(TEXT_SEARCH_URL, params=params, timeout=15)
        data = resp.json()
        status = data.get("status")
        if status == "OK":
            results.extend(data.get("results", []))
        elif status == "ZERO_RESULTS":
            break
        elif status == "OVER_QUERY_LIMIT":
            print("  rate limited, backing off 5s...", file=sys.stderr)
            time.sleep(5)
            continue
        else:
            print(
                f"  text search error for '{query}': {status} "
                f"{data.get('error_message', '')}",
                file=sys.stderr,
            )
            break

        token = data.get("next_page_token")
        if not token:
            break
        # Google requires a short delay before a next_page_token becomes valid.
        time.sleep(2)
        params = {"pagetoken": token, "key": api_key}
        time.sleep(sleep_s)
    return results


def place_details(place_id, api_key, session, sleep_s):
    params = {"place_id": place_id, "fields": DETAILS_FIELDS, "key": api_key}
    resp = session.get(DETAILS_URL, params=params, timeout=15)
    time.sleep(sleep_s)
    data = resp.json()
    if data.get("status") != "OK":
        return None
    return data.get("result")


def is_social_link(url):
    if not url:
        return False
    return any(domain in url.lower() for domain in SOCIAL_DOMAINS)


def load_seen_place_ids(output_path):
    seen = set()
    if os.path.exists(output_path):
        with open(output_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                pid = row.get("place_id")
                if pid:
                    seen.add(pid)
    return seen


def build_row(details, place_id, city, state, query, notes):
    return {
        "business_name": details.get("name", ""),
        "formatted_phone": details.get("formatted_phone_number", ""),
        "international_phone": details.get("international_phone_number", ""),
        "address": details.get("formatted_address", ""),
        "city": city,
        "state": state,
        "google_maps_url": details.get("url", ""),
        "rating": details.get("rating", ""),
        "review_count": details.get("user_ratings_total", ""),
        "place_id": place_id,
        "decision_maker_name": "",
        "decision_maker_role": "",
        "email": "",
        "notes": notes,
        "source_query": query,
        "retrieved_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find US contractors with no website via Google Places API."
    )
    parser.add_argument("--trade", default="general contractor")
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--output", default="leads.csv")
    parser.add_argument(
        "--states", nargs="*", default=None,
        help="Restrict search to these state abbreviations, e.g. CA TX FL",
    )
    parser.add_argument("--max-cities", type=int, default=None)
    parser.add_argument(
        "--strict-no-social", action="store_true",
        help="Also keep leads whose 'website' is actually a Facebook/Yelp/etc. link",
    )
    parser.add_argument("--sleep", type=float, default=0.2)
    parser.add_argument(
        "--resume", action="store_true",
        help="Skip place_ids already present in --output from a prior run",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = load_api_key()
    session = requests.Session()

    cities = US_CITIES
    if args.states:
        wanted = {s.upper() for s in args.states}
        cities = [c for c in cities if c[1] in wanted]
    if args.max_cities:
        cities = cities[: args.max_cities]
    random.shuffle(cities)

    seen_place_ids = load_seen_place_ids(args.output) if args.resume else set()
    append_mode = args.resume and os.path.exists(args.output)
    collected = len(seen_place_ids) if append_mode else 0

    with open(args.output, "a" if append_mode else "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if not append_mode:
            writer.writeheader()

        for city, state in cities:
            if collected >= args.target:
                break
            query = f"{args.trade} in {city}, {state}"
            print(f"[{collected}/{args.target}] searching: {query}", file=sys.stderr)
            results = text_search(query, api_key, session, args.sleep)

            for r in results:
                if collected >= args.target:
                    break
                place_id = r.get("place_id")
                if not place_id or place_id in seen_place_ids:
                    continue
                seen_place_ids.add(place_id)

                details = place_details(place_id, api_key, session, args.sleep)
                if not details or details.get("business_status") != "OPERATIONAL":
                    continue

                website = details.get("website")
                if website:
                    if not (args.strict_no_social and is_social_link(website)):
                        continue
                    notes = (
                        f"No standalone website; listed link is a social/directory "
                        f"page ({website}). Decision-maker/email left blank on "
                        f"purpose - see README."
                    )
                else:
                    notes = (
                        "No website listed on Google Business Profile. "
                        "Decision-maker/email left blank on purpose - see README."
                    )

                row = build_row(details, place_id, city, state, query, notes)
                writer.writerow(row)
                f.flush()
                collected += 1
                print(
                    f"  + lead {collected}: {row['business_name']} ({city}, {state})",
                    file=sys.stderr,
                )

    print(f"Done. {collected} leads written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
