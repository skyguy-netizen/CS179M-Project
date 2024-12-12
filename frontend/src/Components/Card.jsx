import "./Card.css"
import {useState} from 'react'
import PropTypes from "prop-types";

function Card ({handleSubmit}) {
    const [loadName, setLoadName] = useState("")

    const handle = (e) => {
        e.preventDefault();
        handleSubmit(loadName)
        console.log(`Added ${loadName} to load list`)
        setLoadName("");
      }

    return (
        <div className = "card">
            <h2 color = '#0087ff'> Load </h2>
            <h3>Add information about the container</h3>
            <input className = 'con-name'
            type="text"
            value={loadName}
            onChange={(e) => setLoadName(e.target.value)}
            />
            <button className = "button-name" onClick={handle}> Submit </button>
        </div>
    );
}

Card.propTypes = {
    handleSubmit: PropTypes.func.isRequired, 
};

export default Card