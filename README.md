# Douban Movie Data Crawler and Recommendation System

A FastAPI-based system for managing and recommending movies, featuring data crawling from Douban Top 250 and Weekly Charts, with AI-powered recommendations.

## Features

- **Data Crawling**
  - Automatically fetch Douban Top 250 movies
  - Automatically fetch Douban Weekly Trending movies
  - Supports data deduplication and updates
- **Watchlist Management**
  - Mark movies as watched/unwatched
- **Intelligent Recommendation**
  - AI-driven recommendations based on user queries (e.g., "horror movies" or "high-rated")
  - Fallback to highest-rated movies if AI service fails

## Tech Stack

- **Backend**: FastAPI (async support)
- **Database**: MySQL with SQLAlchemy ORM
- **Deployment**: Docker Compose
- **Utilities**:
  - Douban data crawlers (`fetch_top250`, `fetch_one_week`)
  - AI integration (requires custom `call_ai` implementation)

## Access interactive docs at 
- **http://localhost:8000/docs**
- **Core Endpoints**
- Crawl Top250 data	POST	/movies/crawl/top250
- Mark movie as watched	GET	/movies/top250/set_is_watched?id=1&is_watched=true
- Get movie recommendation	POST	/recommend
