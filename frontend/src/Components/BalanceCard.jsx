import "./InfoCard.css"
import PropTypes from "prop-types";

function BalanceCard ({data, index, length}) {
    return (
        <div className = 'card-info'>
          <h2 className = 'steps'> Steps {index + 1} of {length} </h2>
          <h2
          style={{
            'margin-top': '7px'
          }}
          >
           Instructions </h2>
          <h2> Estimated Time: {data.times[index]} minutes </h2>
          <h2> Container: {data.ids[index]} </h2>
          <h2> Source: { JSON.stringify(data.paths[index][0]) } </h2>
          <h2> Destination: { JSON.stringify(data.paths[index][data.paths[index].length - 1]) } </h2> 
        </div>
      );
}

BalanceCard.propTypes = {
    data: PropTypes.object.isRequired, 
    index: PropTypes.number.isRequired, 
    length: PropTypes.number.isRequired, 
  };

export default BalanceCard