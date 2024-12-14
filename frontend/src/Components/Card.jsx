import "./Card.css"
import {useState} from 'react'
import PropTypes from "prop-types";

function Card ({handleSubmit, loadName, setLoadName, loadWeight, setLoadWeight}) {
    const [error, setError] = useState("")

    const handle = (e) => {
        e.preventDefault();
        handleSubmit(loadName, setError)
        console.log(`Added ${loadName} to load list`)
        setLoadName("");
        setLoadWeight("")
      }

    return (
        <div className = "card">
            <h2 color = '#0087ff'> Load </h2>
            <h3>Add information about the container</h3>
            <p>
                Name:
                <input className = 'con-name'
                type="text"
                value={loadName}
                onChange={(e) => setLoadName(e.target.value)}
                />
            </p>
            <p className = "weight">
                Weight:
                <input className = 'con-name'
                type="number"
                value={loadWeight}
                onChange={(e) => setLoadWeight(e.target.value)}
            />
            </p>
            <div className="flex flex-row">
                {error !== "" && <p className="m-4 error">{error}</p>}
                <button onClick={handle} className="flex-1 m-4"> Submit </button>
            </div>
        </div>
    );
}

Card.propTypes = {
    handleSubmit: PropTypes.func.isRequired, 
};

export default Card