import { useEffect, useState } from 'react'
import axios from 'axios';
import Phaser from 'phaser';
import { PhaserGame } from './game/PhaserGame';
import { useRef } from 'react';
import SignInModal from './Components/SignInModal';
import Card from './Components/Card';
import CommentModal from './Components/CommentModal';
import SubmitLoad from './Components/SubmitLoad'

const baseUrl = "http://127.0.0.1:5000"

const LoadPage = () => {
  const[manifest, setManifest] = useState(null)
  const [manifestName, setManifestName] = useState("")
  const [unload, setUnload] = useState([])
  const [load, setLoad] = useState([])
  const [loadName, setLoadName] = useState([])
  const [nextButton, setNextButton] = useState(false)
  const [containerUnloadIndex, setContainerUnloadIndex] = useState(0)
  const [containersToMoveLength, setContainersToMoveLength] = useState(0);
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
        get_fileName()
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  const handleSubmit = (loadName) => {
    setLoad((prevLoad) => [...prevLoad, loadName]); 
    setLoadName(loadName);
    console.log(loadName);
    console.log(`Load updated: ${loadName}`);
    handleAddLoadContainer(); //THIS ADDS THE BLANK BLOCK IN ANIMATION AFTER PRESSING SUBMIT
  };

  const handleLoad = () => {
    const config = {
      headers: {
        "Content-Type": "application/json",
        'Accept' : 'application/json',
      },
    };
    
    console.log(load);
    console.log(unload);
    const data = {load: load, unload: unload};

    axios
      .post(`${baseUrl}/load`, JSON.stringify(data), config)
      .then(response => {
        phaserRef.current.scene.events.emit('move-container', response.data);
        setNextButton(true);
        setContainerUnloadIndex(0);
        setContainersToMoveLength(response.data.ids.length);
        setUnload([]);
        setLoad([]);
      })
      .catch(err=>console.warn(err))
  }

  function handleAnimationChange() {
    setContainerUnloadIndex(containerUnloadIndex+1);
    phaserRef.current.scene.events.emit('next-container');
  }

  function handleAddLoadContainer() {
    phaserRef.current.scene.events.emit('load-container', loadName);
    setLoadName("")
  }


  const get_fileName = () => {
    axios
    .get(`${baseUrl}/get_fileName`)
    .then(async response => {
      console.log(response.data.file_name)
      setManifestName(response.data.file_name)
    })
    .catch(err => {
      console.log(err)
    })
  }

  const get_manifest = () => {
    axios({
        url: `${baseUrl}/manifest`, 
        method: 'GET',
        responseType: 'blob',
    }).then((response) => {
        const href = URL.createObjectURL(response.data);
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', manifestName); 
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
    });
};
  


  return (
    <div className='w-screen h-screen flex justify-center items-center'>
      <SignInModal/>
      {manifest !== null && <PhaserGame ref={phaserRef} currentActiveScene={currentScene} gameData={manifest} updateUnload={setUnload} />}
      <Card 
      handleSubmit={handleSubmit}
      loadName={loadName}
      setLoadName={setLoadName}
      />
      <CommentModal/>
      <SubmitLoad 
      handleLoad={handleLoad}
      />
      <button onClick={get_manifest}> Click </button>
      {(containerUnloadIndex < containersToMoveLength) && <button onClick={handleAnimationChange}>Next</button>}
      </div>
    )
};

export default LoadPage