import { axiosInstance } from './authService';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const TodoService = {
  async getAllTodos() {
    const response = await axiosInstance.get(`${API_URL}/todos/`);
    return response.data;
  },

  async getTodoById(id) {
    const response = await axiosInstance.get(`${API_URL}/todos/${id}`);
    return response.data;
  },

  async createTodo(title, description = '') {
    const response = await axiosInstance.post(`${API_URL}/todos/`, {
      title,
      description,
      completed: false
    });
    return response.data;
  },

  async updateTodoStatus(id, completed) {
    const response = await axiosInstance.put(`${API_URL}/todos/${id}`, {
      completed
    });
    return response.data;
  },


  async deleteTodo(id) {
    const response = await axiosInstance.delete(`${API_URL}/todos/${id}`);
    return response.data;
  }
};

export default TodoService; 