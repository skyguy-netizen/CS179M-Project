import "./InfoCard.css"
import { useState, useEffect } from "react";
import PropTypes from "prop-types";

function InfoCard ({data, index, length}) {
  const [load, setLoad] = useState("");

    useEffect(() => {
      const operation = data.opsOrder[index];
      if (operation === "UL") {
        setLoad("false");
      } else if (operation === "L") {
        setLoad("true");
      }
    }, [data.opsOrder, data.paths, index]);

    function load_path(data) {
      if (load === "true") {
        return JSON.stringify(data.paths[index][data.paths[index].length - 1]); 
      } else if (load === "false") {
        return JSON.stringify(data.paths[index][0]); 
      }
      return ""; 
    }

    function allTime() {
      let total = 0;
      for(let i = index; i < data.times.length; ++i) {
        total += data.times[i];
      }
      return total;
    }

    return (
        <div className = 'card-info'>
          <h2 className = 'steps'> Steps {index + 1} of {length} </h2>
          <h2
          style={{
            'margin-top': '7px'
          }}
          > { load === "true" ? "Load" : "Unload" } </h2>
          <h3> Overall Time Remaining: {allTime()} minutes </h3>
          <h3> Estimated Time: {data.times[index]} minutes </h3>
          <h3> Container: {data.ids[index]} </h3>
          <h3> Source: { load === "true" ? "Truck" : load_path(data) } </h3>
          <h3> Destination: { load === "true" ? load_path(data) : "Truck" } </h3> 
        </div>
      );
}

InfoCard.propTypes = {
    data: PropTypes.object.isRequired, 
    index: PropTypes.number.isRequired, 
    length: PropTypes.number.isRequired, 
  };

export default InfoCard