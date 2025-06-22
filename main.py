from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
import httpx

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/api/outline")
async def get_country_outline(country: str = Query(..., description="Country name")):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": f"Could not fetch Wikipedia page for '{country}'."}

    soup = BeautifulSoup(response.text, "html.parser")
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    outline = "## Contents\n\n"
    for heading in headings:
        level = int(heading.name[1])
        title = heading.text.strip()
        outline += f"{'#' * level} {title}\n\n"

    return {"country": country, "markdown_outline": outline.strip()}
