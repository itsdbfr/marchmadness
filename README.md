# March Madness Data Analysis

This project scrapes NCAA basketball statistics for March Madness tournament analysis, collecting both coaching records and player performance data from official NCAA statistics.

## Overview

The project consists of two main scrapers that collect comprehensive basketball data:
- **Coach statistics**: Career records, win-loss percentages, and tenure information
- **Player statistics**: Scoring leaders, three-point performance, and game statistics

## Files

- `Coach Stats Scraper.py` - Scrapes coaching statistics from NCAA head coaches database
- `Player Stats Scraper.py` - Scrapes player scoring statistics from NCAA active career leaders
- `CoachData.xlsx` - Output file containing comprehensive coach statistics
- `TopScorerData2025.xlsx` - Output file containing top scorer data and performance metrics

## Features

### Coach Data Collection
- Scrapes all NCAA basketball head coaches (434+ pages)
- Collects career statistics including total seasons, wins, losses, and win-loss percentage
- Tracks coaching tenure and current team information
- Handles retired coaches appropriately

### Player Data Collection
- Scrapes NCAA active career scoring leaders
- Collects comprehensive scoring statistics including total points, three-pointers, and averages
- Tracks games played and performance metrics
- Supports historical data collection across multiple seasons

## Requirements

```
selenium
pandas
openpyxl
webdriver-manager
```

Install dependencies:
```bash
pip install selenium pandas openpyxl webdriver-manager
```

## Usage

1. **Run the Coach Stats Scraper:**
   ```bash
   python "Coach Stats Scraper.py"
   ```
   - Scrapes all NCAA basketball head coaches
   - Generates `CoachData.xlsx` with comprehensive coaching statistics

2. **Run the Player Stats Scraper:**
   ```bash
   python "Player Stats Scraper.py"
   ```
   - Scrapes NCAA active career scoring leaders
   - Generates `TopScorerData2025.xlsx` with player performance data

## Data Sources

- **Coach Data**: [NCAA Head Coaches Database](https://stats.ncaa.org/head_coaches)
- **Player Data**: [NCAA Active Career Leaders](https://stats.ncaa.org/active_career_leaders/view_rankings?id=2916608)

## Output Data

### Coach Statistics (`CoachData.xlsx`)
- Coach Name
- Total Seasons
- Total Wins
- Total Losses
- Win-Loss Percentage
- All Tenures
- Current Team

### Player Statistics (`TopScorerData2025.xlsx`)
- Year
- Rank
- Player Name
- Team
- Division
- Points Scored
- Three Pointers Scored
- Average Points Scored
- Games Played

## Technical Features

- **Robust Error Handling**: Implements retry mechanisms for stale element exceptions
- **Rate Limiting**: Uses random sleep intervals to avoid overwhelming servers
- **Pagination Support**: Automatically navigates through multiple pages of results
- **Dynamic Content Handling**: Uses Selenium WebDriver for JavaScript-rendered content
- **Data Validation**: Handles missing data and retired coaches appropriately

## Notes

- The scrapers use Chrome WebDriver (automatically managed by webdriver-manager)
- Random sleep intervals (1-4 seconds) are implemented to be respectful to NCAA servers
- File paths are currently set to `/Users/db/Desktop/Fordham/March Madness/Python/` - update as needed
- Coach scraper processes 434+ pages of data (approximately 10,000+ coaches)
- Player scraper currently configured for 2 pages of top scorers (200 players)

## Future Enhancements

- Add support for multiple seasons of player data
- Implement team-specific filtering
- Add tournament performance metrics
- Create data visualization components
- Add historical trend analysis
