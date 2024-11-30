import React from 'react'
import Modal from './Components/SignInModal';
import UploadModal from './Components/UploadModal';

const NavButtonUpload = ({Icon}) => {
  return (
    <div className='flex flex-col items-center'>
      <button className='bg-white rounded-full w-48 h-48 flex justify-center items-center'>
        <Icon/>
      </button>
      <h2 className='mt-4 text-[#0087ff]'>{"Upload"}</h2>
      <UploadModal/>
    </div>
  )
}

export default NavButtonUpload