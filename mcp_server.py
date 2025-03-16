from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
from typing import List, Optional
import logging
from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GitHub API Explorer",
    description="A FastAPI app to fetch GitHub data with a nice UI.",
    version="1.0.0"
)

# Initialize Jinja2 templates
templates = Jinja2Templates(directory="templates")

# GitHub API Authentication
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment variables")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Rate limiting
CALLS_PER_MINUTE = 60
PERIOD = 60

# Pydantic models
class RepoResponse(BaseModel):
    name: str
    description: Optional[str] = "No description provided"
    url: str
    language: Optional[str] = "Not specified"

class CommitResponse(BaseModel):
    message: str
    author: str
    date: str

class IssueResponse(BaseModel):
    title: str
    url: str
    state: str
    created_at: str

# Helper function for API requests
@sleep_and_retry
@limits(calls=CALLS_PER_MINUTE, period=PERIOD)
def github_api_request(url: str) -> dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise HTTPException(status_code=503, detail=f"GitHub API error: {str(e)}")

# Endpoint to fetch user repositories (HTML + JSON)
@app.get("/get-repos", response_class=HTMLResponse)
async def get_repos(request: Request, as_json: bool = False):
    """Fetch all repositories for the authenticated GitHub user."""
    url = "https://api.github.com/user/repos"
    try:
        repos = github_api_request(url)
        formatted_repos = [
            {
                "name": repo["name"],
                "description": repo["description"],
                "url": repo["html_url"],
                "language": repo["language"]
            }
            for repo in repos
        ]
        if as_json:
            return JSONResponse(content=jsonable_encoder(formatted_repos))
        return templates.TemplateResponse(
            "repos.html", {"request": request, "repos": formatted_repos}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_repos: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to fetch commits (HTML + JSON)
@app.get("/get-commits", response_class=HTMLResponse)
async def get_commits(request: Request, owner: str, repo: str, as_json: bool = False):
    """Fetch commits from a specified GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    try:
        commits = github_api_request(url)
        formatted_commits = [
            {
                "message": commit["commit"]["message"],
                "author": commit["commit"]["author"]["name"],
                "date": commit["commit"]["author"]["date"]
            }
            for commit in commits
        ]
        if as_json:
            return JSONResponse(content=jsonable_encoder(formatted_commits))
        return templates.TemplateResponse(
            "commits.html", {"request": request, "commits": formatted_commits, "owner": owner, "repo": repo}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_commits: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to fetch issues (HTML + JSON)
@app.get("/get-issues", response_class=HTMLResponse)
async def get_issues(request: Request, owner: str, repo: str, as_json: bool = False):
    """Fetch open issues from a specified GitHub repository."""
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    try:
        issues = github_api_request(url)
        formatted_issues = [
            {
                "title": issue["title"],
                "url": issue["html_url"],
                "state": issue["state"],
                "created_at": issue["created_at"]
            }
            for issue in issues
        ]
        if as_json:
            return JSONResponse(content=jsonable_encoder(formatted_issues))
        return templates.TemplateResponse(
            "issues.html", {"request": request, "issues": formatted_issues, "owner": owner, "repo": repo}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in get_issues: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)