// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import axios from 'axios';
import "./ModalLogIn.css";

const baseUrl = "http://127.0.0.1:5000"

export default function SignInModal() {
  const [modal, setModal] = useState(false);
  const [signedInName, setSignedInName] = useState(""); 
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
    setSignedInName(firstName);

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
        {signedInName === "" ? "Sign In" :  signedInName}
      </button>

      {modal && (
        <div className="modal">
          <div onClick={toggleModal} className="overlay"></div>
          <div className="modal-content">
            <h2 className="modal-sign"> Sign In</h2>
            <p className="modal-input">
              Name:  
              <input 
                type="text"
                id="firstName"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
              />
            </p>
            <button className="close-modal" onClick={toggleModal}>
              Close
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