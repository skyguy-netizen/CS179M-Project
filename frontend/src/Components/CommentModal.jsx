// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import axios from 'axios';
import "./Comment.css";

const baseUrl = "http://127.0.0.1:5000"

export default function CommentModal() {
  const [modal, setModal] = useState(false);
  const [comment, setComment] = useState("");

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
    
    const data = {comment: comment};

    axios
      .post(`${baseUrl}/comment`, JSON.stringify(data), config)
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
        Add comment to log
      </button>

      {modal && (
        <div className="modal">
          <div onClick={toggleModal} className="overlay"></div>
          <div className="modal-content">
            <h2 className="modal-sign"> Sign In</h2>
            <p className="modal-input">
              Add Comment:  
              <input 
                type="text"
                id="comment"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              />
            </p>
            <button className="close-modal" onClick={toggleModal}>
              Close
            </button>
            <button className="log-modal" onClick={handleName}>
              Submit
            </button>
          </div>
        </div>
      )}
    </>
  );
}