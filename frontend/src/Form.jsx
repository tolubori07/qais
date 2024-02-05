/* eslint-disable react/no-unescaped-entities */

import { useState } from 'react';

const Form = () => {
  const [numberOfSupports, setNumberOfSupports] = useState('');
  const [numberOfInternalJoints, setNumberOfInternalJoints] = useState('');
  const [spans, setSpans] = useState([]);

  const handleInputChange = (index, e) => {
    const { name, value } = e.target;
    const updatedSpans = [...spans];
    updatedSpans[index][name] = value;
    setSpans(updatedSpans);
  };

  const handleLoadingConditionChange = (index, e) => {
    const { value } = e.target;
    const updatedSpans = [...spans];
    updatedSpans[index]['loadingCondition'] = value;
    setSpans(updatedSpans);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Here you can send the form data to the Django API
    // You can use the 'spans' state to send the data for each span
    console.log(spans);
  };

  const calculateNumberOfSpans = () => {
    const numSupports = parseInt(numberOfSupports);
    const numInternalJoints = parseInt(numberOfInternalJoints);
    const numNodes = numSupports + numInternalJoints;
    const numSpans = numNodes - 1;
    const initialSpans = Array(numSpans).fill({
      spanLength: '',
      load: '',
      loadingCondition: '',
    }).map(span => ({ ...span })); // Ensure each span object is unique
    setSpans(initialSpans);
  };

  return (
    <form className="max-w-md mx-auto my-8 p-8 bg-white shadow-lg rounded" onSubmit={handleSubmit}>
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Number of Supports:</label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          type="number"
          value={numberOfSupports}
          onChange={(e) => setNumberOfSupports(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-bold mb-2">Number of Internal Joints:</label>
        <input
          className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          type="number"
          value={numberOfInternalJoints}
          onChange={(e) => setNumberOfInternalJoints(e.target.value)}
        />
      </div>

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="button"
        onClick={calculateNumberOfSpans}
      >
        Calculate Number of Spans
      </button>

      <hr className="my-4" />

      {spans.map((span, index) => (
        <div key={index} className="mb-4">
          <h2 className="text-xl font-bold">Span {index + 1}</h2>

          <label className="block text-gray-700 text-sm font-bold mb-2">Span Length:</label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="number"
            name="spanLength"
            value={span.spanLength || ''}
            onChange={(e) => handleInputChange(index, e)}
          />

          <label className="block text-gray-700 text-sm font-bold mb-2">Load:</label>
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="number"
            name="load"
            value={span.load || ''}
            onChange={(e) => handleInputChange(index, e)}
          />

          <label className="block text-gray-700 text-sm font-bold mb-2">Loading Condition:</label>
          <select
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            name="loadingCondition"
            value={span.loadingCondition || ''}
            onChange={(e) => handleLoadingConditionChange(index, e)}
          >
            <option value="">Select Loading Condition</option>
            <option value="P_C">Point load at center (P_C)</option>
            <option value="P_X">Point load at distance 'a' from left end and 'b' from the right end (P_X)</option>
            <option value="P_C_2">Two equal point loads, spaced at 1/3 of the total length from each other (P_C_2)</option>
            <option value="P_C_3">Three equal point loads, spaced at 1/4 of the total length from each other (P_C_3)</option>
            <option value="UDL">Uniformly distributed load over the whole length (UDL)</option>
            <option value="UDL/2_R">Uniformly distributed load over half of the span on the right side (UDL/2_R)</option>
            <option value="UDL/2_L">Uniformly distributed load over half of the span on the left side (UDL/2_L)</option>
            <option value="VDL_R">Variably distributed load, with the highest point on the right end (VDL_R)</option>
            <option value="VDL_L">Variably distributed load, with the highest point on the left end (VDL_L)</option>
            <option value="VDL_C">Variably distributed load, with the highest point at the center (VDL_C)</option>
          </select>

          {/* Add more fields as needed */}
        </div>
      ))}

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
        type="submit"
      >
        Submit
      </button>
    </form>
  );
};

export default Form;
