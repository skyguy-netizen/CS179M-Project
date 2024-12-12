// Credit: https://github.com/ecole-du-web/react-modal

import { useState } from "react";
import axios from 'axios';
import "./Modal.css";
import LoadIcon from '../assets/load.svg?react'
import { useNavigate } from "react-router";

const baseUrl = "http://127.0.0.1:5000"

export default function LoadModal() {
  const navigate = useNavigate();
  const [modal, setModal] = useState(false);
  const [file, setFile] = useState();

  const toggleModal = () => {
    setModal(!modal);
  };

  function handleUpload(event) {
    if(!file) {
      console.log("No file selected");
      return;
    }

    event.preventDefault();
    const formData = new FormData();
    formData.append('file', file);
    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };

    axios
      .post(`${baseUrl}/fileUploadLoad`, formData, config)
      .then(() => {
        navigate("/LoadPage")
      })
      .catch(err=>console.warn(err))

    toggleModal()
  }

  if(modal) {
    document.body.classList.add('active-modal')
  } else {
    document.body.classList.remove('active-modal')
  }

  return (
    <>
      <div className='flex flex-col items-center'>
        <button onClick={toggleModal} className='bg-white rounded-full w-48 h-48 flex justify-center items-center'>
          <LoadIcon/>
        </button>
      <h2 className='mt-4 text-[#0087ff]'>{"Load/Unload"}</h2>
      </div>

      {modal && (
        <div className="modal">
          <div onClick={toggleModal} className="overlay"></div>
          <div className="modal-content">
            <h2 className='modal-file'> {"Upload File"}</h2>
            <p>
              <input className='modal-input' onChange = { (e) => setFile(e.target.files[0]) } type="file"/>
            </p>
            <button className="close-modal" onClick={toggleModal}>
              Close
            </button>
            <button className="log-modal" onClick={handleUpload}>
              Submit
            </button>
          </div>
        </div>
      )}
    </>
  );
}