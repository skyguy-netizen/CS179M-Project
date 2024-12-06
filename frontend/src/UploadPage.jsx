import { useEffect, useState } from 'react'
import axios from 'axios';
import Phaser from 'phaser';
import { PhaserGame } from './game/PhaserGame';
import { useRef } from 'react';

const baseUrl = "http://127.0.0.1:5000"

const LoadPage = () => {
  const[manifest, setManifest] = useState(null)
  const [unload, setUnload] = useState([])
  const [load, setLoad] = useState([])
  const [loadName, setLoadName] = useState("")

  const [canMoveSprite, setCanMoveSprite] = useState(true);
    
    //  References to the PhaserGame component (game and scene are exposed)
    const phaserRef = useRef();
    const [spritePosition, setSpritePosition] = useState({ x: 0, y: 0 });

    // Event emitted from the PhaserGame component
    const currentScene = (scene) => {

        setCanMoveSprite(scene.scene.key !== 'MainMenu');
        
    }

  useEffect(() => {
    axios
      .get(`${baseUrl}/fileUploadLoad`)
      .then(async response => {
        setManifest(response.data)
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoad(load.concat(loadName));
    console.log(`Added ${loadName} to load list`)
    setLoadName("");
  }

  function handleLoad(event) {
    event.preventDefault()

    const config = {
      headers: {
        "Content-Type": "application/json",
        'Accept' : 'application/json',
      },
    };
    
    const data = {load: load, unload: unload};

    axios
      .post(`${baseUrl}/load`, JSON.stringify(data), config)
      .then(response => response.json())
      .then(console.log(unload))
      .then(console.log(load))
      .catch(err=>console.warn(err))
  }

  return (
    <div className='w-screen h-screen flex justify-center items-center'>
      {manifest !== null && <PhaserGame ref={phaserRef} currentActiveScene={currentScene} gameData={manifest} updateUnload={setUnload} />}
      <button onClick={handleLoad}>Send</button>
      <form onSubmit={handleSubmit}>
        <input
        type="text"
        value={loadName}
        onChange={(e) => {
          setLoadName(e.target.value)
        }}
        />
        <button type="submit">Load</button>
      </form>
    </div>
  )
}

export default LoadPage