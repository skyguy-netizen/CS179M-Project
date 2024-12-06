import LoadModal from './Components/LoadModal'
import BalanceModal from './Components/BalanceModal'
import SignInModal from './Components/SignInModal'

const LandingPage = () => {
  return (
    <>
    <SignInModal/>
    <div className='flex flex-center justify-center p-4'>
      <h1>DockerTech Co.</h1>
    </div>
    <div className='h-screen overflow-hidden items-center flex'>
      <div className='flex justify-center space-x-40 w-screen mb-32'>
        <LoadModal/>
        <BalanceModal/>
      </div>
    </div>
    </>
  )
}

export default LandingPage