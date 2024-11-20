import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [events, setEvents] = useState([]);
  const [newEvent, setNewEvent] = useState({ name: '', location: '' });

  // Al cargar el componente, se cargan los eventos desde la API
  useEffect(() => {
    axios.get('http://localhost:8080/events/')
      .then(response => {
        setEvents(response.data);
      })
      .catch(error => {
        console.error("Error fetching events:", error);
      });
  }, []);

  // Manejar cambios en el formulario de creación de eventos
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewEvent(prevState => ({ ...prevState, [name]: value }));
  };

  // Manejar el envío del formulario para crear un nuevo evento
  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post('http://localhost:8080/events/', newEvent)
      .then(response => {
        setEvents([...events, response.data]);
        setNewEvent({ name: '', location: '' });
      })
      .catch(error => {
        console.error("Error creating event:", error);
      });
  };

  return (
    <div>
      <h1>Event List</h1>
      <ul>
        {events.map(event => (
          <li key={event.id}>{event.name} - {event.location}</li>
        ))}
      </ul>

      <h2>Create Event</h2>
      <form onSubmit={handleSubmit}>
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
  );
}

export default App;
