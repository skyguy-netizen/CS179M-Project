import "./InfoCard.css"
import { useState, useEffect } from "react";
import PropTypes from "prop-types";

function InfoCard ({data, index}) {
  const [load, setLoad] = useState("");
  const [string, setString] = useState("");


    useEffect(() => {
      const operation = data.opsOrder[index];
      if (operation === "UL") {
        setLoad("true");
      } else if (operation === "L") {
        setLoad("false");
      }
      setString(JSON.stringify(data.paths[index]))
    }, [data.opsOrder, data.paths, index]);
  

    function load_path(data) {
      if (load === "true") {
        return JSON.stringify(data.paths[index][0]); 
      } else if (load === "false") {
        return JSON.stringify(data.paths[index][string.length - 1]);
      }
      return ""; 
    }

    return (
        <div className = 'card-info'>
          <h2> { load === "true" ? "Unload" : "Load" } </h2>
          <h2> Estimated Time: {data.times[index]} minutes </h2>
          <h2> Container: {data.ids[index]} </h2>
          <h2> Source: { load === true ? "Truck" : load_path(data) } </h2>
          <h2> Destination: { load === true ? load_path(data) : "Truck" } </h2> 
        </div>
      );
}

InfoCard.propTypes = {
    data: PropTypes.object.isRequired, 
    index: PropTypes.number.isRequired, 
  };

export default InfoCard