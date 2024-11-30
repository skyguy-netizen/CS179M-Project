import React from 'react'
import NavButton from './NavButtons'
import UploadIcon from './assets/upload.svg?react'
import LoadIcon from './assets/load.svg?react'
import BalanceIcon from './assets/balance.svg?react'

const LandingPage = () => {
  return (
    <>
    <div className='flex flex-center justify-center p-4'>
      <h1>DockerTech Co.</h1>
    </div>
    <div className='h-screen overflow-hidden items-center flex'>
      <div className='flex justify-center space-x-40 w-screen mb-32'>
        <NavButton Icon={UploadIcon} Text="Upload"/>
        <NavButton Icon={LoadIcon} Text="Load/Unload"/>
        <NavButton Icon={BalanceIcon} Text="Balance"/>
      </div>
    </div>
    </>
  )
}

export default LandingPage