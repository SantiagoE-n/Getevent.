import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'user', // Rol por defecto
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState(''); // Estado para éxito
  const navigate = useNavigate();

  // Manejar cambios en el formulario
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  // Enviar formulario de registro
  const handleSubmit = (e) => {
    e.preventDefault();
    setError(''); // Limpiar errores previos
    setSuccess(''); // Limpiar mensajes previos de éxito

    axios.post('http://localhost:8000/register/', formData)
      .then((response) => {
        console.log('Registration successful:', response.data);
        setSuccess('Registration successful! You can now log in.');
        setTimeout(() => navigate('/'), 2000); // Redirigir después de 2 segundos
      })
      .catch(err => {
        console.error('Registration error:', err);
        setError('Failed to register. Please check your inputs and try again.');
      });
  };

  return (
    <div className="register-container">
      <h2>Register</h2>
      <form onSubmit={handleSubmit} className="register-form">
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <select name="role" value={formData.role} onChange={handleChange}>
          <option value="user">User</option>
          <option value="organizer">Organizer</option>
        </select>
        <button type="submit">Register</button>
        {success && <p style={{ color: 'green' }}>{success}</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
};

export default Register;