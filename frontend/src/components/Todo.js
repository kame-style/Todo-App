import React from 'react';
import '../styles/Todo.css';

/**
 * Component representing a single Todo item
 * 
 * @param {Object} props - Component props
 * @param {Object} props.todo - The todo item data
 * @param {Function} props.onToggle - Function to toggle the completion status
 * @param {Function} props.onDelete - Function to delete the todo
 */
const Todo = ({ todo, onToggle, onDelete }) => {
  // Format date for better display
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  return (
    <li className={todo.completed ? 'completed' : ''}>
      <div className="todo-content">
        <h3>{todo.title}</h3>
        {todo.description && <p>{todo.description}</p>}
        <div className="todo-meta">
          Created: {formatDate(todo.created_at)}
          {todo.updated_at && (
            <span> • Updated: {formatDate(todo.updated_at)}</span>
          )}
        </div>
      </div>
      <div className="todo-actions">
        <button
          className={`toggle-btn ${todo.completed ? 'completed' : ''}`}
          onClick={() => onToggle(todo.id, todo.completed)}
        >
          {todo.completed ? 'Mark Incomplete' : 'Mark Complete'}
        </button>
        <button
          className="delete-btn"
          onClick={() => onDelete(todo.id)}
        >
          Delete
        </button>
      </div>
    </li>
  );
};

export default Todo; 