import re

from bs4 import BeautifulSoup
import httpx

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


async def fetch_top250():
    base_url = "https://movie.douban.com/top250"
    movies = []

    timeout = httpx.Timeout(10.0, connect=5.0)
    limits = httpx.Limits(max_connections=8, max_keepalive_connections=4)
    async with httpx.AsyncClient(headers=HEADERS, timeout=timeout, limits=limits) as client:
        for start in range(0, 250, 25):
            url = f"{base_url}?start={start}"
            resp = await client.get(url)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select("div.item"):
                title = item.select_one("span.title").text.strip()
                rating = float(item.select_one("span.rating_num").text)

                quote_tag = item.select_one("p.quote span")
                introduction = quote_tag.text.strip() if quote_tag else ""

                bd_p = item.select_one("div.bd p")
                info = bd_p.text.strip().split("\n")[0]
                director = info.split("主演")[0].replace("导演:", "").strip()
                actors = info.split("主演:")[-1].strip() if "主演:" in info else ""

                rank = int(item.select_one("div.pic em").text)

                movies.append({
                    "rank": rank,
                    "title": title,
                    "rating": rating,
                    "director": director,
                    "actors": actors,
                    "introduction": introduction
                })

        return movies


async def fetch_one_week():
    url = "https://movie.douban.com/chart"
    movies = []

    timeout = httpx.Timeout(10.0, connect=5.0)
    limits = httpx.Limits(max_connections=8, max_keepalive_connections=4)
    async with httpx.AsyncClient(headers=HEADERS, timeout=timeout, limits=limits) as client:
        resp = await client.get(url)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("tr.item")

        for idx, item in enumerate(rows, start=1):
            title = item.select_one("a.nbg")["title"].strip()
            rating_tag = item.select_one("span.rating_nums")
            rating = float(rating_tag.text) if rating_tag else 0.0

            intro_tag = item.select_one("div.pl2 p")
            introduction = intro_tag.text.strip() if intro_tag else ""

            parts = [seg.strip() for seg in (intro_tag.text.split("/") if intro_tag else [])]
            date_segs = [seg for seg in parts if re.match(r"\d{4}-\d{2}-\d{2}", seg)]
            release_date = date_segs[0] if date_segs else ""

            rest = parts[len(date_segs):]
            actors_list = []
            for seg in rest:
                if re.search(r"\d|分钟", seg):
                    break
                actors_list.append(seg)
            actors = ", ".join(actors_list)

            movies.append({
                "rank": idx,
                "title": title,
                "rating": rating,
                "release_date": release_date,
                "actors": actors,
                "introduction": introduction
            })

    return movies