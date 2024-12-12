// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import axios from 'axios';
import "./Comment.css";

const baseUrl = "http://127.0.0.1:5000"

export default function CommentModal() {
  const [modal_com, setModal_com] = useState(false);
  const [comment_, setComment] = useState("");

  const toggleModal = () => {
    setModal_com(!modal_com);
  };

  function handleName(event) {
    event.preventDefault()

    const config = {
      headers: {
        "Content-Type": "application/json",
        'Accept' : 'application/json, text/plain, */*',
      },
    };
    
    const data = {comment: comment_};

    axios
      .post(`${baseUrl}/comment`, JSON.stringify(data), config)
      .then(response => response.json())
      .catch(err=>console.warn(err))

    toggleModal();
  }

  if(modal_com) {
    document.body.classList.add('active-com-modal')
  } else {
    document.body.classList.remove('active-com-modal')
  }

  return (
    <>
      <button onClick={toggleModal} className="btn-modal-com" color = '#0087ff'>
        Add Comment To Log
      </button>

      {modal_com && (
        <div className="modal-com">
          <div onClick={toggleModal} className="overlay-com"></div>
          <div className="modal-com-content">
            <h2 className="modal-com-sign"> Comment</h2>
            <h3>Add Comment To Log:  </h3>
            <p className="modal-com-input">
              <input 
                type="text"
                id="comment_"
                value={comment_}
                onChange={(e) => setComment(e.target.value)}
                style={{width: "370px"}}
              />
            </p>
            <button className="close-com-modal" onClick={toggleModal}>
              Close
            </button>
            <button className="log-com-modal" onClick={handleName}>
              Submit 
            </button>
          </div>
        </div>
      )}
    </>
  );
}