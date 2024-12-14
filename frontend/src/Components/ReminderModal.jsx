// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import "./SubmitLoad.css";
import { useNavigate } from "react-router";

function ReminderModal() {
  const [modal_load, setModal_load] = useState(false);
  const navigate = useNavigate();

  const toggleModal = () => {
    setModal_load(!modal_load);
  };

  const toggleComplete = () => {
    setModal_load(!modal_load);
    navigate("/")
  };

  if(modal_load) {
    document.body.classList.add('active-load-modal')
  } else {
    document.body.classList.remove('active-load-modal')
  }

  return (
    <>
      <button onClick={toggleModal} className="btn-modal-load">
        Completed Cycle
      </button>

      {modal_load && (
        <div className="modal-load">
          <div onClick={toggleModal} className="overlay-load"></div>
          <div className="modal-load-content">
            <h2 className="modal-load-sign"> Completed Cycle </h2>
            <h3>Click complete if you have downloaded and sent the OUTBOUND manifest to the ship </h3>
            <button className="close-load-modal" onClick={toggleModal}>
              Close
            </button>
            <button className="log-load-modal" onClick={toggleComplete}>
              Complete
            </button>
          </div>
        </div>
      )}
    </>
  );
}
export default ReminderModal