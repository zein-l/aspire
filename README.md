# My Recipes App

A modular Flask application for managing recipes. Users can add, edit, delete, search, and categorize recipes. Bonus features include multi-user support and simple AI suggestions.

## Features

### Core
- **Recipe CRUD**: Create, read, update, delete recipes with fields:
  - Name  
  - Ingredients  
  - Instructions  
  - Prep time  
  - Cuisine  
  - Status (`to-write`, `to-try`, `made before`)
- **Search**: Filter by name, ingredient, cuisine, or maximum prep time.  
- **Status management**: Quickly switch recipe status via buttons.

### Bonus
- **Multi-user**: Register, log in, and manage your own recipes.  
- **AI suggestions**: Endpoint that uses a simple HuggingFace pipeline to predict cuisine or suggest status based on ingredients.  
- **Extras**: Easily add tags, ratings, image uploads, or custom features.

## Setup & Run

1. **Clone the repo** (or initialize and push local if empty):
  
   git clone https://github.com/zein-l/aspire.git
   cd my_recipes_app

Create & activate a virtual environment:


python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
Install dependencies:


pip install -r requirements.txt
# For development/testing:
pip install -r requirements-dev.txt
Configure environment variables:
Copy .env.example to .env and edit:


FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///recipes.db
Initialize the database:


flask db init
flask db migrate -m "Initial schema"
flask db upgrade
Run the server:


python run.py
Open your browser at http://localhost:5000 (or your LAN IP).