import "./InfoCard.css"
import PropTypes from "prop-types";

function BalanceCard ({data, index, length}) {

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
          >
           Instructions </h2>
          <h3> Overall Time Remaining: {allTime()} minutes </h3>
          <h3> Estimated Move Time: {data.times[index]} minutes </h3>
          <h3> Container: {data.ids[index]} </h3>
          <h3> Source: { JSON.stringify(data.paths[index][0]) } </h3>
          <h3> Destination: { JSON.stringify(data.paths[index][data.paths[index].length - 1]) } </h3> 
        </div>
      );
}

BalanceCard.propTypes = {
    data: PropTypes.object.isRequired, 
    index: PropTypes.number.isRequired, 
    length: PropTypes.number.isRequired, 
  };

export default BalanceCard