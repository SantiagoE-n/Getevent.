import React, { useState, useEffect, useCallback } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import axios from 'axios';
import Modal from 'react-modal';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faSignOutAlt, faBars } from '@fortawesome/free-solid-svg-icons';
import './App.css';
import './EventList.css';
import Register from './Register';

Modal.setAppElement('#root'); // Evita errores de accesibilidad en React Modal.

function App() {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ name: '', location: '', date: new Date() });
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [token, setToken] = useState(localStorage.getItem('access_token') || '');
  const [role, setRole] = useState(localStorage.getItem('role') || '');
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [loginError, setLoginError] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);

  // Obtener eventos
  const fetchEvents = useCallback(() => {
    axios.get('http://localhost:8000/events/', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(response => {
        console.log("Fetched Events:", response.data.events);
        setEvents(response.data.events);
      })
      .catch(error => {
        console.error("Error fetching events:", error);
        if (error.response?.status === 401) handleLogout();
      });
  }, [token]);

  useEffect(() => {
    if (token) fetchEvents();
  }, [token, fetchEvents]);

  const handleInputChange = (e) => setNewEvent({ ...newEvent, [e.target.name]: e.target.value });
  const handleDateChange = (date) => setNewEvent({ ...newEvent, date });
  const handleLoginChange = (e) => setCredentials({ ...credentials, [e.target.name]: e.target.value });

  // Login
  const handleLoginSubmit = (e) => {
    e.preventDefault();
    setLoginError('');
    axios.post('http://localhost:8000/token/', credentials)
      .then(response => {
        const { access } = response.data;
        setToken(access);
        localStorage.setItem('access_token', access);

        axios.get('http://localhost:8000/profile/', {
          headers: { Authorization: `Bearer ${access}` }
        }).then(res => {
          console.log("User Role:", res.data.role);
          setRole(res.data.role);
          localStorage.setItem('role', res.data.role);
          setLoginError('');
          alert("Login Successful!");
        }).catch(() => setLoginError("Error fetching user profile."));
      })
      .catch(() => setLoginError("Invalid username or password. Please try again."));
  };

  const handleEventSubmit = (e) => {
    e.preventDefault();
    console.log("Creating Event:", newEvent);
    axios.post('http://localhost:8000/events/create/', newEvent, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(() => {
        console.log("Event created successfully!");
        fetchEvents();
        setModalIsOpen(false);
        setNewEvent({ name: '', location: '', date: new Date() });
        alert("Event created successfully!");
      })
      .catch((err) => {
        console.error("Error creating event:", err);
        alert("Error creating event.");
      });
  };

  const handleLogout = () => {
    setToken('');
    setRole('');
    localStorage.removeItem('access_token');
    localStorage.removeItem('role');
    setEvents([]);
  };

  const toggleMenu = () => setMenuOpen(!menuOpen);

  return (
    <Router>
      <div className="app-container">
        {/* Header */}
        <header className="app-header">
          <h1>Event List</h1>
          <button className="menu-btn" onClick={toggleMenu}>
            <FontAwesomeIcon icon={faBars} />
          </button>
          {token ? (
            <button className="logout-btn" onClick={handleLogout}>
              <FontAwesomeIcon icon={faSignOutAlt} /> Logout
            </button>
          ) : (
            <Link to="/register" className="register-link">Register</Link>
          )}
          {menuOpen && (
            <nav className="responsive-menu">
              <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/register">Register</Link></li>
              </ul>
            </nav>
          )}
        </header>

        {/* Main Content */}
        <main className="app-main">
          <Routes>
            <Route
              path="/"
              element={!token ? (
                <div className="login-form">
                  <h2>Login</h2>
                  <form onSubmit={handleLoginSubmit}>
                    <input type="text" name="username" placeholder="Username" onChange={handleLoginChange} value={credentials.username} required />
                    <input type="password" name="password" placeholder="Password" onChange={handleLoginChange} value={credentials.password} required />
                    <button type="submit">Login</button>
                  </form>
                  {loginError && <p className="error-message" style={{ color: "red" }}>{loginError}</p>}
                </div>
              ) : (
                <>
                  {role === 'organizer' && (
                    <>
                      <button className="add-btn" onClick={() => setModalIsOpen(true)}>
                        <FontAwesomeIcon icon={faPlus} /> Add Event
                      </button>
                      <h2>My Events</h2>
                      <ul className="event-list">
                        {events.map(event => (
                          <li key={event.id}>
                            <span>{event.name}</span> - <span>{event.location}</span> - <span>{new Date(event.date).toLocaleDateString()}</span>
                          </li>
                        ))}
                      </ul>
                      <Modal
                        isOpen={modalIsOpen}
                        onRequestClose={() => setModalIsOpen(false)}
                        ariaHideApp={false}
                        className="ReactModal__Content"
                        overlayClassName="ReactModal__Overlay"
                      >
                        <h2>Create Event</h2>
                        <img src="https://via.placeholder.com/300" alt="Event Preview" className="responsive-img" />
                        <form onSubmit={handleEventSubmit}>
                          <input type="text" name="name" placeholder="Event Name" onChange={handleInputChange} required />
                          <input type="text" name="location" placeholder="Location" onChange={handleInputChange} required />
                          <DatePicker selected={newEvent.date} onChange={handleDateChange} dateFormat="yyyy-MM-dd" />
                          <button type="submit">Create</button>
                          <button type="button" onClick={() => setModalIsOpen(false)}>Cancel</button>
                        </form>
                      </Modal>
                    </>
                  )}
                </>
              )}
            />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="app-footer">
          <p>&copy; 2024 GetEvent. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;