import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

function App() {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ name: '', location: '' });
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [token, setToken] = useState(localStorage.getItem('access_token') || ''); // Cargar token si existe

  // Función para obtener eventos desde la API
  const fetchEvents = useCallback(() => {
    axios.get('http://localhost:8000/events/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(response => {
        setEvents(response.data.events);
      })
      .catch(error => {
        console.error("Error fetching events:", error);
        if (error.response && error.response.status === 401) {
          alert("Session expired! Please log in again.");
          handleLogout();
        }
      });
  }, [token]); // Token es la dependencia necesaria

  // Al cargar el componente, cargar eventos si el token está presente
  useEffect(() => {
    if (token) fetchEvents();
  }, [token, fetchEvents]);

  // Manejar cambios en el formulario de creación de eventos
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEvent(prevState => ({ ...prevState, [name]: value }));
  };

  // Manejar cambios en el formulario de inicio de sesión
  const handleLoginChange = (e) => {
    const { name, value } = e.target;
    setCredentials({ ...credentials, [name]: value });
  };

  // Enviar las credenciales al backend para obtener el token
  const handleLoginSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:8000/token/', credentials)
      .then(response => {
        setToken(response.data.access);
        localStorage.setItem('access_token', response.data.access); // Guardar token en localStorage
        alert("Login Successful! Token has been set.");
      })
      .catch(error => {
        console.error("Login failed:", error);
        alert("Login failed! Check your credentials.");
      });
  };

  // Manejar el envío del formulario para crear un nuevo evento
  const handleEventSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:8000/events/create/', newEvent, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(response => {
        setEvents([...events, response.data.event]);
        setNewEvent({ name: '', location: '' });
      })
      .catch(error => {
        console.error("Error creating event:", error);
        alert("Error creating event! Make sure you're logged in.");
      });
  };

  // Manejar Logout
  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('access_token');
    setEvents([]);
    alert("You have been logged out.");
  };

  return (
    <div>
      <h1>Event List</h1>
      {!token ? (
        <div>
          <h2>Login</h2>
          <form onSubmit={handleLoginSubmit}>
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={credentials.username}
              onChange={handleLoginChange}
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={credentials.password}
              onChange={handleLoginChange}
            />
            <button type="submit">Login</button>
          </form>
        </div>
      ) : (
        <div>
          <button onClick={handleLogout} style={{ marginBottom: '20px' }}>Logout</button>
          
          <ul>
            {events.map(event => (
              <li key={event.id}>{event.name} - {event.location}</li>
            ))}
          </ul>

          <h2>Create Event</h2>
          <form onSubmit={handleEventSubmit}>
            <input
              type="text"
              name="name"
              placeholder="Event Name"
              value={newEvent.name}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="location"
              placeholder="Event Location"
              value={newEvent.location}
              onChange={handleInputChange}
            />
            <button type="submit">Create Event</button>
          </form>
        </div>
      )}
    </div>
  );
}

export default App;