import { useEffect, useState } from 'react'
import axios from 'axios';
import Phaser from 'phaser';
import { PhaserGame } from './game/PhaserGame';
import { useRef } from 'react';
import SignInModal from './Components/SignInModal';
import Card from './Components/Card';
import CommentModal from './Components/CommentModal';
import SubmitLoad from './Components/SubmitLoad';
import InfoCard from './Components/InfoCard';
import ReminderModal from './Components/ReminderModal';
import BalanceCard from './Components/BalanceCard';

const baseUrl = "http://127.0.0.1:5000"

const BalancePage = () => {
  const [manifest, setManifest] = useState(null)
  const [manifestName, setManifestName] = useState("")
  const [nextButton, setNextButton] = useState(false)
  const [containerUnloadIndex, setContainerUnloadIndex] = useState(0)
  const [containersToMoveLength, setContainersToMoveLength] = useState(0);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [data, setData] = useState({ paths: [], ids: [], times: [], opsOrder: [] });
  const [index, setIndex] = useState(0);

  const [canMoveSprite, setCanMoveSprite] = useState(true);
  const [isBalanced, setIsBalanced] = useState(false);
    
    //  References to the PhaserGame component (game and scene are exposed)
    const phaserRef = useRef();
    const [spritePosition, setSpritePosition] = useState({ x: 0, y: 0 });

    // Event emitted from the PhaserGame component
    const currentScene = (scene) => {
      setCanMoveSprite(scene.scene.key !== 'MainMenu');
        
    }

  useEffect(() => {
    axios
      .get(`${baseUrl}/fileUploadBalance`)
      .then(async response => {
        setManifest(response.data)
        get_fileName()
      })
      .catch(err => {
        console.log(err)
      })
  }, [])

  const checkBalance = () => {
    axios
      .get(`${baseUrl}/checkbalance`)
      .then((response) => {
        setIsBalanced(response.data.balance === 0);
        console.log(`Balaned? ${response.data.balance}`);
      })
      .catch((err) => console.warn(err));
  };


  useEffect(() => {
    checkBalance();
  }, []);
  
  const startBalanceComputation = () => {
    if (balanceSteps.length > 0) {
      setCurrentBalanceStep(0);
      setNextButton(true); // Enable step-by-step balancing
    }
  };
  
  const handleBalanceStep = () => {
    if (currentBalanceStep < balanceSteps.length) {
      // Emit balance step to Phaser scene
      phaserRef.current.scene.events.emit('balance-step', balanceSteps[currentBalanceStep]);
      setCurrentBalanceStep((prev) => prev + 1);
      
      // Check if it's the last step
      if (currentBalanceStep === balanceSteps.length - 1) {
        setIsBalanced(true); // Grid is balanced
        setNextButton(false); // Disable further steps
      }
    }
  };
  

  const fetchBalanceSteps = () => {
    const config = {
      headers: {
        "Content-Type": "application/json",
        'Accept' : 'application/json',
      },
    };

    axios
      .post(`${baseUrl}/balance`, config)
      .then(response => {
        phaserRef.current.scene.events.emit('move-container', response.data);
        setNextButton(true);
        setContainerUnloadIndex(0);
        setContainersToMoveLength(response.data.ids.length);
        setIsSubmitted(true);
        setData(response.data)
        setIndex(0)
      })
      .catch(err=>console.warn(err))
  }

  function handleAnimationChange() {
    setContainerUnloadIndex(containerUnloadIndex+1);
    setIndex(index + 1)
    checkBalance();
    phaserRef.current.scene.events.emit('next-container');
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
        get_fileName()
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
      {manifest !== null && <PhaserGame ref={phaserRef} currentActiveScene={currentScene} gameData={manifest}/>}
      <CommentModal/>

        {!isSubmitted && (
          <button 
            className='compute-button' 
            onClick={fetchBalanceSteps}
            style={{
              padding: '8px 20px',
              position: 'relative',
              'text-align': 'right',
              top: '10%',
              right: '0%',
              'max-width': '290px',
              'min-width': '120px',
              height: '55px',
              display: 'block',
              margin: '0 auto',
              'font-size': '18px',
              color:'hsla(0,0%,0%)',
              background: 'hsla(0,0%,80%)',
              'border-radius': '3px'
            }}
          >
            Compute
          </button>
        )}

      {isSubmitted && (containerUnloadIndex >= containersToMoveLength) && <ReminderModal/>}
      
      {isSubmitted && (containerUnloadIndex >= containersToMoveLength) && <p 
        className = "txt-modal-manifest"
        style={{
          color: "green",
          fontSize: "18px",
          fontWeight: "bold",
          position: "absolute",
          top: "50%",
          right: "15%",
          transform: "translate(-50%, -50%)",
        }}>
        Balanced! 
      </p>}

      {isSubmitted && (containerUnloadIndex >= containersToMoveLength) && <button 
        className = "btn-modal-manifest" 
        onClick={get_manifest}
        style={{
          color: "#0087ff",
          background: "#f1f1f1",
          width:"10%",
          height:"65px",
          top: "35%", 
          right: "10%",
          position: "absolute",
          'border-radius': "3px",
          'font-size': '18px',
          display: 'block',
          fontWeight: 'bold',
        }}>
        Download Manifest 
      </button>}

      {(containerUnloadIndex < containersToMoveLength)  && <BalanceCard data={data} index={index} length={data.ids.length}/>}

      {(containerUnloadIndex < containersToMoveLength) && 
      <button 
        onClick={handleAnimationChange}
        style={{
          padding: '8px 20px',
          position: 'relative',
          'text-align': 'right',
          top: '10%',     
          right: '0%',
          'max-width': '290px',
          'min-width': '80px',
          height: '55px',
          display: 'block',
          margin: '0 auto',
          'font-size': '18px',
          color: 'hsla(0,0%,0%)',
          background: 'hsla(0,0%,80%)',
          'border-radius': '3px'
        }}
        >
        Next
      </button>}

    </div>
  )
}

export default BalancePage