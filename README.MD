# GitHub Metrics Project

This project calculates and prints metrics related to pull requests on a GitHub repository, including average time per author.

## Getting Started

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repository.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repository
   ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. Create a .env file in the project root with the following content:

    ```bash
    GITHUB_OWNER=your_username
    GITHUB_REPO=your_repository
    GITHUB_TOKEN=your_personal_access_token
    START_DATE=2024-01-01
    END_DATE=2024-01-31
    ```

    Replace the placeholder values with your actual GitHub username, repository name, and personal access token. Adjust the start and end dates as needed.

2. Run the script:

    ```bash
    python github_metrics.py
    ```

3. View the calculated metrics in the console.
