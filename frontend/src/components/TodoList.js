import React from 'react';
import Todo from './Todo';
import '../styles/TodoList.css';

/**
 * Component to display a list of Todo items
 * 
 * @param {Object} props - Component props
 * @param {Array} props.todos - Array of todo items
 * @param {Function} props.onToggleTodo - Function to toggle the completion status of a todo
 * @param {Function} props.onDeleteTodo - Function to delete a todo
 */
const TodoList = ({ todos, onToggleTodo, onDeleteTodo }) => {
  // Show a message when there are no todos
  if (todos.length === 0) {
    return <div className="no-todos">No todos yet. Add one above!</div>;
  }

  return (
    <div className="todo-list">
      <h2>Your Todos</h2>
      <ul>
        {todos.map((todo) => (
          <Todo 
            key={todo.id} 
            todo={todo} 
            onToggle={onToggleTodo} 
            onDelete={onDeleteTodo} 
          />
        ))}
      </ul>
    </div>
  );
};

export default TodoList; 