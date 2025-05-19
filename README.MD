# Virtual Judge

This is a FastAPI-based online judge system for programming problems. It allows users to submit code solutions to predefined problems and automatically evaluates them against test cases.

## Features

- Create and manage programming problems with custom test cases
- Submit solutions in Python programming language
- Automatic evaluation of submissions against test cases
- PostgreSQL database integration with SQLAlchemy ORM
- Environment variable configuration

## Project Structure

```
.
├── .env                  # Environment variables
├── judge.db              # SQLite database (fallback)
├── requirements.txt      # Python dependencies
├── run.sh                # Shell script to run the application
├── test_virtual_judge.http # HTTP requests for testing
└── app/                  # Main application package
    ├── __init__.py
    ├── database.py       # Database connection and configuration
    ├── judge.py          # Code evaluation logic
    ├── main.py           # FastAPI application initialization
    ├── models.py         # SQLAlchemy models
    ├── run.py            # Application entry point
    └── routers/          # API routes
        ├── __init__.py
        ├── problems.py   # Problem management endpoints
        └── submissions.py # Code submission endpoints
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd virtual-judge
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the database:
   - By default, the application uses PostgreSQL. You can modify the `.env` file to change database settings.
   - Uncomment the SQLite configuration in `app/database.py` if you prefer using SQLite.

5. Run the application:
```bash
# Using run.sh script
./run.sh

# Or using Python directly
python -m app.run
```

The application will be available at http://localhost:8000.

## API Endpoints

### Problems

- `GET /problems/` - List all problems
- `GET /problems/{problem_id}` - Get a specific problem with its test cases
- `POST /problems/` - Create a new problem with test cases

### Submissions

- `POST /submit/` - Submit code for evaluation

## Example Usage

You can use the included `test_virtual_judge.http` file to test the API endpoints. If you have the REST Client extension in Visual Studio Code, you can send requests directly from the editor.

## Environment Variables

Configure these variables in the `.env` file:

- `DATABASE_URL` - Database connection string (PostgreSQL or SQLite)
- `PORT` - Server port (default: 8000)
