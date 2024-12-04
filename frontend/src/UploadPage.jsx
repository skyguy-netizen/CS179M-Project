import { useEffect, useState } from 'react'
import axios from 'axios';
import SignInModal from './Components/SignInModal';

const baseUrl = "http://127.0.0.1:5000"

const LoadPage = () => {
  const[manifest, setManifest] = useState({})

  useEffect(() => {
    axios
      .get(`${baseUrl}/fileUpload`)
      .then(async response => {
        setManifest(response.data)
        console.log(response.data)
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  return (
    <div> LoadPage
      <SignInModal/>
      <h3> {manifest.message} </h3>
    </div>
  )
}

export default LoadPage