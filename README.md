# CineWhisper - Movie Recommendation DRF API

CineWhisper is a robust backend system for a movie recommendation web application. This project is designed to simulate real-world backend development scenarios with a strong focus on performance, security, and modular architecture.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)


## Features


### Core Functionality
- **Movie Recommendations API:**  
  - Fetch trending movies and personalized recommendations by integrating with [TMDb](https://www.themoviedb.org/documentation/api).
  - Robust error handling and caching using Redis.
- **User Management:**  
  - JWT-based authentication for secure access.
  - Endpoints for user registration, login, and managing favorite movies.
- **First-Time User Experience:**  
  - New users receive default recommendations (e.g., popular movies) before setting personal preferences.

### Technical Enhancements
- **Database Optimization:**  
  - Optimized PostgreSQL schema and queries.
- **API Documentation:**  
  - Interactive Swagger/OpenAPI documentation for easy integration.
- **Security:**  
  - Secure token management and role-based permissions.


## Architecture

### Project Structure
```bash
├ core/
├ movies/
├ users/
├ docs/ 
├ manage.py
├ requirements.txt
├ .env
└ README.md
```


## Tech Stack

- **Backend:** Python 3.12, Django 4.2
- **API Framework:** Django REST Framework (DRF)
- **Database:** PostgreSQL
- **Caching:** Redis
- **Authentication:** JWT (using Simple JWT)
- **Documentation:** Swagger/OpenAPI


## Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis
- Virtual Environment (e.g., venv)
- *(Optional)* Docker & Docker Compose


### Installation

#### Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/CineWhisper.git
cd CineWhisper

# Copy the environment variables file
cp .envs/.env.example .env

# Build Docker images and start the containers
docker-compose up --build -d

# Run database migrations
docker-compose exec web python manage.py migrate

# Create a superuser for admin access
docker-compose exec web python manage.py createsuperuser
```

#### Manual Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/CineWhisper.git
cd CineWhisper

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .envs/.env.example .env

# Run migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```


## API Documentation

Interactive API documentation is available at:

- **Swagger UI:** [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
- **ReDoc:** [http://localhost:8000/api/docs/redoc/](http://localhost:8000/api/docs/redoc/)


## Hosted Instance

A live version of CineWhisper is hosted at:

- **CineWhisper Live:** [https://cinewhisper.up.railway.app](https://cinewhisper.up.railway.app)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create your feature branch:
   ```bash
    git flow feature start <feature-name>
   ```
3. Commit Your Changes
   ```bash
    git add .
    git commit -m "feat: describe your changes"
   ```
4. Push Your Branch to your fork
   ```bash
    git push origin feature/<feature-name>
   ```
5. Open a Pull Request
   On GitHub, open a pull request from your feature branch into the develop branch of the main repository.


## License
This project is licensed under the MIT License.


## Support
For support or any questions, please email ajiboseibrahim12@gmail.com or open an issue in the repository.
