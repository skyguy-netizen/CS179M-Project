import React from 'react'
import { useEffect } from 'react'
import axios from 'axios';

const baseUrl = "http://127.0.0.1:5000"

const LoadPage = () => {

  useEffect(() => {
    console.log("test")
    axios
        .get(`${baseUrl}/manifest`)
        .then(response => {
            console.log(response)
        })
        .catch(err => {
            console.log(err)
        })
  }, [])

  return (
    <div>LoadPage</div>
  )
}

export default LoadPage