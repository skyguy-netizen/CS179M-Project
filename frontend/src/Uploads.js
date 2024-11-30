import React, {useState} from 'react';
import axios from 'axios';
import Modal from './Components/Modal';

const baseUrl = "http://127.0.0.1:5000"

function Uploads(){
  const [file, setFile] = useState();
  
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
      .post(`${baseUrl}/fileUpload`, formData, config)
      .catch(err=>console.warn(err))
  }
  return (
    <div>
      <h1 className="Welcome"> 
       <input onChange = { (e) => setFile(e.target.files[0]) } type="file"/>
       <button onClick={handleUpload}> Upload </button> 
      </h1>
      <Modal />
    </div>
  );
}

export default App;