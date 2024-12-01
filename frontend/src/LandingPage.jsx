import LoadModal from './components/LoadModal'
import BalanceModal from './components/BalanceModal'
import SignInModal from './components/SignInModal'

const LandingPage = () => {
  return (
    <>
    <div className='flex flex-center justify-center p-4'>
      <h1>DockerTech Co.</h1>
    </div>
    <div className='h-screen overflow-hidden items-center flex'>
      <div className='flex justify-center space-x-40 w-screen mb-32'>
        <LoadModal/>
        <BalanceModal/>
        <SignInModal/>
      </div>
    </div>
    </>
  )
}

export default LandingPage