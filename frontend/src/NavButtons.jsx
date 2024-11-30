import React from 'react'

const NavButton = ({Icon, Text}) => {
  return (
    <div className='flex flex-col items-center'>
      <button className='bg-white rounded-full w-48 h-48 flex justify-center items-center'>
        <Icon/>
      </button>
      <h2 className='mt-4 text-[#0087ff]'>{Text}</h2>
    </div>
  )
}

export default NavButton