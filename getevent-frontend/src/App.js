import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Modal from 'react-modal';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import './App.css';

Modal.setAppElement('#root'); // Requerido por react-modal

function App() {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ name: '', location: '', date: new Date() });
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [token, setToken] = useState(localStorage.getItem('access_token') || '');
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [loginError, setLoginError] = useState(''); // Estado para errores de login

  // Función para obtener eventos
  const fetchEvents = useCallback(() => {
    axios.get('http://localhost:8000/events/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(response => setEvents(response.data.events))
      .catch(error => {
        console.error("Error fetching events:", error);
        if (error.response?.status === 401) handleLogout();
      });
  }, [token]);

  // Cargar eventos si el token existe
  useEffect(() => { if (token) fetchEvents(); }, [token, fetchEvents]);

  const handleInputChange = (e) => setNewEvent({ ...newEvent, [e.target.name]: e.target.value });

  const handleDateChange = (date) => setNewEvent({ ...newEvent, date });

  const handleLoginChange = (e) => setCredentials({ ...credentials, [e.target.name]: e.target.value });

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    setLoginError(''); // Limpiar errores previos
    axios.post('http://localhost:8000/token/', credentials)
      .then(response => {
        setToken(response.data.access);
        localStorage.setItem('access_token', response.data.access);
        setLoginError(''); // Limpiar errores
        alert("Login Successful!");
      })
      .catch((error) => {
        console.error("Login error:", error);
        setLoginError("Invalid username or password. Please try again.");
      });
  };

  const handleEventSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:8000/events/create/', newEvent, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(() => {
        fetchEvents();
        setModalIsOpen(false);
        setNewEvent({ name: '', location: '', date: new Date() });
      })
      .catch(() => alert("Error creating event."));
  };

  const handleLogout = () => {
    setToken('');
    localStorage.removeItem('access_token');
    setEvents([]);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <h1>Event List</h1>
        {token && (
          <button className="logout-btn" onClick={handleLogout}>
            <FontAwesomeIcon icon={faSignOutAlt} /> Logout
          </button>
        )}
      </header>

      {/* Main Content */}
      <main className="app-main">
        {!token ? (
          <div className="login-form">
            <h2>Login</h2>
            <form onSubmit={handleLoginSubmit}>
              <input
                type="text"
                name="username"
                placeholder="Username"
                onChange={handleLoginChange}
                value={credentials.username}
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                onChange={handleLoginChange}
                value={credentials.password}
                required
              />
              <button type="submit">Login</button>
            </form>
            {/* Mostrar error de login */}
            {loginError && <p className="error-message" style={{ color: "red" }}>{loginError}</p>}
          </div>
        ) : (
          <div>
            <button className="add-btn" onClick={() => setModalIsOpen(true)}>
              <FontAwesomeIcon icon={faPlus} /> Add Event
            </button>

            {/* Event List */}
            <ul className="event-list">
              {events.map(event => (
                <li key={event.id}>
                  <span>{event.name}</span> - <span>{event.location}</span> - <span>{new Date(event.date).toLocaleDateString()}</span>
                </li>
              ))}
            </ul>

            {/* Modal for Creating Events */}
            <Modal
              isOpen={modalIsOpen}
              onRequestClose={() => setModalIsOpen(false)}
              className="modal"
              overlayClassName="modal-overlay"
            >
              <h2>Create Event</h2>
              <form onSubmit={handleEventSubmit}>
                <input type="text" name="name" placeholder="Event Name" onChange={handleInputChange} required />
                <input type="text" name="location" placeholder="Location" onChange={handleInputChange} required />
                <DatePicker selected={newEvent.date} onChange={handleDateChange} />
                <button type="submit">Create</button>
              </form>
            </Modal>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>&copy; 2024 GetEvent. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;