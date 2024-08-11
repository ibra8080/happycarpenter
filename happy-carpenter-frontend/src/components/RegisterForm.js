import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegisterForm() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password1, setPassword1] = useState('');
  const [password2, setPassword2] = useState('');
  const [errors, setErrors] = useState({});

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('/dj-rest-auth/registration/', {
        username,
        email,
        password1,
        password2
      });
      // Handle successful registration
      console.log(response.data);
      navigate('/login');
    } catch (err) {
      console.log(err.response?.data);
      setErrors(err.response?.data);
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group controlId="username">
        <Form.Label>Username</Form.Label>
        <Form.Control 
          type="text" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </Form.Group>
      {errors.username?.map((message, idx) => (
        <Alert variant="warning" key={idx}>{message}</Alert>
      ))}

      <Form.Group controlId="email">
        <Form.Label>Email</Form.Label>
        <Form.Control 
          type="email" 
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </Form.Group>
      {errors.email?.map((message, idx) => (
        <Alert variant="warning" key={idx}>{message}</Alert>
      ))}

      <Form.Group controlId="password1">
        <Form.Label>Password</Form.Label>
        <Form.Control 
          type="password" 
          value={password1}
          onChange={(e) => setPassword1(e.target.value)}
        />
      </Form.Group>
      {errors.password1?.map((message, idx) => (
        <Alert variant="warning" key={idx}>{message}</Alert>
      ))}

      <Form.Group controlId="password2">
        <Form.Label>Confirm Password</Form.Label>
        <Form.Control 
          type="password" 
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
      </Form.Group>
      {errors.password2?.map((message, idx) => (
        <Alert variant="warning" key={idx}>{message}</Alert>
      ))}

      <Button type="submit">Register</Button>
    </Form>
  );
}

export default RegisterForm;