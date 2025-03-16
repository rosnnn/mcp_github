###MCP GitHub API Server###


#Overview
-->The MCP GitHub API Server is a lightweight and scalable backend application powered by FastAPI. It    simplifies interactions with the GitHub API by providing accessible endpoints to retrieve repository information, commit history, and open issues.

This tool is perfect for developers and teams who want to access GitHub data programmatically in an intuitive and streamlined way.

#Features
-->Get Repositories: Fetch details of GitHub repositories for an authenticated user.

-->Get Commits: Retrieve the commit history for any GitHub repository.

-->Get Issues: View a list of open issues for a specific repository.

-->Fast and Lightweight: Built with FastAPI and served via Uvicorn for blazing performance.



#Technologies Used
*Language: Python 3.13

*Framework: FastAPI

*Server: Uvicorn

*API: GitHub REST API



#Setup Instructions
1. Clone the Repository
bash
git clone <your-repository-url>
cd <repo-folder>
2. Create a Virtual Environment
bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root of the project and add your GitHub Personal Access Token (PAT):

GITHUB_TOKEN=your_personal_access_token OR, set it directly in your terminal:

bash
export GITHUB_TOKEN=your_personal_access_token
# On Windows:
set GITHUB_TOKEN=your_personal_access_token
5. Start the Server
bash
uvicorn mcp_server:app --reload
6. Access the API
The API will be available at:

http://127.0.0.1:8000



#Endpoints

1. Get Repositories
URL: /get-repos

Method: GET

Description: Fetches a list of repositories for the authenticated user.

Example Response:

json
[
    {
        "Name": "sample-repo",
        "Description": "This is a sample repository",
        "URL": "https://github.com/username/sample-repo",
        "Language": "Python"
    }
]

2. Get Commits
URL: /get-commits?owner={owner}&repo={repo}

Method: GET

Description: Retrieves commit history for the specified repository.

Query Parameters:

owner: GitHub username of the repository owner.

repo: Name of the repository.

Example Response:

json
[
    {
        "Message": "Initial commit",
        "Author": "username",
        "Date": "2025-03-15T10:00:00Z"
    }
]



3. Get Issues
URL: /get-issues?owner={owner}&repo={repo}

Method: GET

Description: Retrieves open issues for the specified repository.

Query Parameters:

owner: GitHub username of the repository owner.

repo: Name of the repository.

Example Response:

json
[
    {
        "Title": "Bug in authentication",
        "URL": "https://github.com/username/sample-repo/issues/1",
        "State": "open",
        "Created At": "2025-03-14T08:30:00Z"
    }
]

Contribution Guidelines (Optional)
We welcome contributions! Follow these steps to contribute:

Fork the repository.

Create a new branch:

bash
git checkout -b feature/your-feature-name
Commit your changes:

bash
git commit -m "Add your feature"
Push to your branch:

bash
git push origin feature/your-feature-name
Submit a pull request.


###############
###BackToTop###
###############
