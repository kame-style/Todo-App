import React, { useState, useEffect } from 'react';
import './styles/App.css';
import TodoList from './components/TodoList';
import TodoForm from './components/TodoForm';
import AuthPage from './components/AuthPage';
import todoService from './services/todoService';
import { AuthService } from './services/authService';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(AuthService.isLoggedIn());
  const [user, setUser] = useState(null);

  const fetchUserInfo = async () => {
    try {
      const response = await AuthService.getCurrentUser();
      setUser(response.data);
    } catch (err) {
      console.error('Error fetching user info:', err);
      // If we can't get user info, user might be logged out or token expired
      if (err.response?.status === 401) {
        AuthService.logout();
        setIsAuthenticated(false);
      }
    }
  };

  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await todoService.getAllTodos();
      setTodos(data);
    } catch (err) {
      console.error('Error fetching todos:', err);
      // If unauthorized, redirect to login
      if (err.response?.status === 401) {
        AuthService.logout();
        setIsAuthenticated(false);
        setError('Your session has expired. Please login again.');
      } else {
        setError('Failed to fetch todos. Please try again later.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchUserInfo();
      fetchTodos();
    } else {
      setTodos([]);
      setUser(null);
      setLoading(false);
    }
  }, [isAuthenticated]);

  const handleAuthSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    AuthService.logout();
    setIsAuthenticated(false);
    setTodos([]);
    setUser(null);
  };

  const addTodo = async (title, description = '') => {
    try {
      setError(null);
      const newTodo = await todoService.createTodo(title, description);
      setTodos(prevTodos => [...prevTodos, newTodo]);
    } catch (err) {
      console.error('Error adding todo:', err);
      if (err.response?.status === 401) {
        AuthService.logout();
        setIsAuthenticated(false);
        setError('Your session has expired. Please login again.');
      } else {
        setError('Failed to add todo. Please try again.');
      }
    }
  };

  const toggleTodo = async (id, completed) => {
    try {
      setError(null);
      const updatedTodo = await todoService.updateTodoStatus(id, !completed);
      setTodos(prevTodos => 
        prevTodos.map(todo => todo.id === id ? updatedTodo : todo)
      );
    } catch (err) {
      console.error('Error updating todo:', err);
      if (err.response?.status === 401) {
        AuthService.logout();
        setIsAuthenticated(false);
        setError('Your session has expired. Please login again.');
      } else {
        setError('Failed to update todo. Please try again.');
      }
    }
  };

  const deleteTodo = async (id) => {
    try {
      setError(null);
      await todoService.deleteTodo(id);
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
    } catch (err) {
      console.error('Error deleting todo:', err);
      if (err.response?.status === 401) {
        AuthService.logout();
        setIsAuthenticated(false);
        setError('Your session has expired. Please login again.');
      } else {
        setError('Failed to delete todo. Please try again.');
      }
    }
  };

  const handleRetry = () => {
    fetchTodos();
  };

  if (!isAuthenticated) {
    return (
      <div className="App">
        <header className="App-header">
          <h1>Todo App</h1>
        </header>
        <main>
          <AuthPage onAuthSuccess={handleAuthSuccess} />
        </main>
        <footer className="App-footer">
          <p>Todo App &copy; {new Date().getFullYear()}</p>
        </footer>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Todo App</h1>
        {user && (
          <div className="user-info">
            <span>Welcome, {user.email}!</span>
            <button onClick={handleLogout} className="logout-btn">Logout</button>
          </div>
        )}
      </header>
      <main>
        <TodoForm onAddTodo={addTodo} />
        
        {error && (
          <div className="error">
            <p>{error}</p>
            <button onClick={handleRetry} className="retry-btn">Retry</button>
          </div>
        )}
        
        {loading ? (
          <div className="loading">
            <p>Loading your todos...</p>
            <div className="loading-spinner"></div>
          </div>
        ) : (
          <TodoList 
            todos={todos} 
            onToggleTodo={toggleTodo} 
            onDeleteTodo={deleteTodo}
          />
        )}
      </main>
      <footer className="App-footer">
        <p>Todo App &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App; 