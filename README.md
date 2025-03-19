# Todo List Application

A simple Todo List application built with React, FastAPI, PostgreSQL, and Docker.

## Technologies Used

- **Frontend**: React with JavaScript
- **Backend**: Python FastAPI with Pydantic
- **Database**: PostgreSQL with SQLAlchemy
- **Containerization**: Docker and Docker Compose

## Project Structure

```
Todo-app/
├── frontend/            # React frontend
├── backend/             # FastAPI backend
└── docker-compose.yml   # Docker Compose configuration
```

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Node.js and npm (if running without Docker)
- Python 3.8+ and pip (if running without Docker)
- PostgreSQL (if running without Docker)
- WSL2 (if using Windows)

## Running the Application

### Using Docker Compose (Recommended)

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/Todo-app.git
   cd Todo-app
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Running Locally (Without Docker)

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a .env file with your database connection details)

5. Start the backend server:
   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Access the frontend at http://localhost:3000

## Building for Production

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create a production build:
   ```bash
   npm run build
   ```

3. The build artifacts will be stored in the `build` directory

### Backend

1. For production, it's recommended to use a production ASGI server like Uvicorn with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -k uvicorn.workers.UvicornWorker main:app
   ```

## Deployment

### Docker Deployment

1. Build and tag Docker images:
   ```bash
   docker-compose build
   ```

2. Push images to your container registry:
   ```bash
   docker-compose push
   ```

### Deploying to a Cloud Provider

#### Heroku

1. Install the Heroku CLI and log in:
   ```bash
   heroku login
   ```

2. Create Heroku apps for both frontend and backend:
   ```bash
   heroku create todo-app-frontend
   heroku create todo-app-backend
   ```

3. Set up PostgreSQL database:
   ```bash
   heroku addons:create heroku-postgresql --app todo-app-backend
   ```

4. Deploy the backend:
   ```bash
   cd backend
   git init
   heroku git:remote -a todo-app-backend
   git add .
   git commit -m "Initial backend deployment"
   git push heroku master
   ```

5. Deploy the frontend:
   ```bash
   cd frontend
   # Update the API_URL in src/services/todoService.js to point to your backend URL
   npm run build
   # Use the Heroku buildpack for Create React App
   heroku buildpacks:set https://github.com/mars/create-react-app-buildpack.git --app todo-app-frontend
   git init
   heroku git:remote -a todo-app-frontend
   git add .
   git commit -m "Initial frontend deployment"
   git push heroku master
   ```

#### AWS/Azure/GCP

For cloud providers like AWS, Azure, or GCP, you can:
1. Use container services like AWS ECS, Azure Container Instances, or Google Cloud Run
2. Deploy the Docker images to these services
3. Set up a managed database service
4. Configure environment variables for API connections

## Features

- Create, read, update, and delete todo items
- Mark todos as complete or incomplete
- Responsive UI design

## API Endpoints

- `GET /todos/`: Get all todo items
- `GET /todos/{todo_id}`: Get a specific todo item
- `POST /todos/`: Create a new todo item
- `PUT /todos/{todo_id}`: Update a todo item
- `DELETE /todos/{todo_id}`: Delete a todo item

## Troubleshooting

- **CORS Issues**: Ensure the backend has CORS properly configured
- **Database Connection**: Check database connection strings in environment variables
- **Port Conflicts**: Make sure ports 3000 and 8000 are available, or configure different ports

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request 



jwt based auth
sign up and verification
email based


- chat bot with langchain, 
agentic AI
Langchain

