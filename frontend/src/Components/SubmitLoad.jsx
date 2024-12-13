// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import "./SubmitLoad.css";
import PropTypes from "prop-types";

function SubmitLoad({handleLoad}) {
  const [modal_load, setModal_load] = useState(false);

  const handle = (e) => {
      e.preventDefault();
      handleLoad()
      setModal_load(!modal_load);
    }

  const toggleModal = () => {
    setModal_load(!modal_load);
  };

  if(modal_load) {
    document.body.classList.add('active-load-modal')
  } else {
    document.body.classList.remove('active-load-modal')
  }

  return (
    <>
      <button onClick={toggleModal} className="btn-modal-load">
        Compute
      </button>

      {modal_load && (
        <div className="modal-load">
          <div onClick={toggleModal} className="overlay-load"></div>
          <div className="modal-load-content">
            <h2 className="modal-load-sign"> Compute </h2>
            <h3>Click submit if all containers to be unloaded/loaded have been accounted for.</h3>
            <button className="close-load-modal" onClick={toggleModal}>
              Close
            </button>
            <button 
              className="log-load-modal" 
              onClick={handle}
            >
              Submit
            </button>
          </div>
        </div>
      )}
    </>
  );
}

SubmitLoad.propTypes = {
  handleLoad: PropTypes.func.isRequired, 
};

export default SubmitLoad