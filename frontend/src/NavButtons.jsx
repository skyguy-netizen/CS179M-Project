import React from 'react'
import { Link } from 'react-router-dom'

const NavButton = ({Icon, Text}) => {
  return (
    <div className='flex flex-col items-center'>
      <Link to="/LoadPage" className='bg-white rounded-full w-48 h-48 flex justify-center items-center'>
        <Icon/>
      </Link>
      <h2 className='mt-4 text-[#0087ff]'>{Text}</h2>
    </div>
  )
}

export default NavButton