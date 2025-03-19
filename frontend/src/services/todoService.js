import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const TodoService = {
  async getAllTodos() {
    const response = await axios.get(`${API_URL}/todos/`);
    return response.data;
  },

  async getTodoById(id) {
    const response = await axios.get(`${API_URL}/todos/${id}`);
    return response.data;
  },

  async createTodo(title, description = '') {
    const response = await axios.post(`${API_URL}/todos/`, {
      title,
      description,
      completed: false
    });
    return response.data;
  },

  async updateTodoStatus(id, completed) {
    const response = await axios.put(`${API_URL}/todos/${id}`, {
      completed
    });
    return response.data;
  },


  async deleteTodo(id) {
    const response = await axios.delete(`${API_URL}/todos/${id}`);
    return response.data;
  }
};

export default TodoService; 