// Credit: https://github.com/ecole-du-web/react-modal

import React, { useState } from "react";
import axios from 'axios';
import "./Modal.css";

const baseUrl = "http://127.0.0.1:5000"

export default function SignInModal() {
  const [modal, setModal] = useState(false);
  const [firstName, setFirstName] = useState("");

  const toggleModal = () => {
    setModal(!modal);
  };

  function handleName(event) {
    event.preventDefault()

    const config = {
      headers: {
        "Content-Type": "application/json",
        'Accept' : 'application/json, text/plain, */*',
      },
    };
    
    const data = {first_name: firstName};

    axios
      .post(`${baseUrl}/login`, JSON.stringify(data), config)
      .then(response => response.json())
      .catch(err=>console.warn(err))

    toggleModal();
  }

  if(modal) {
    document.body.classList.add('active-modal')
  } else {
    document.body.classList.remove('active-modal')
  }

  return (
    <>
      <button onClick={toggleModal} className="btn-modal">
        Log In
      </button>

      {modal && (
        <div className="modal">
          <div onClick={toggleModal} className="overlay"></div>
          <div className="modal-content">
            <h2>Sign In</h2>
            <p>
              Name: 
              <input 
                type="text"
                id="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </p>
            <button className="close-modal" onClick={toggleModal}>
              CLOSE
            </button>
            <button className="log-modal" onClick={handleName}>
              Log In
            </button>
          </div>
        </div>
      )}
    </>
  );
}