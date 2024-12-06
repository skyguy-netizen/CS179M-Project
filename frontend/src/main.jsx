import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage.jsx';
import LoadPage from './UploadPage.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
                <Route path="/LoadPage" element={<LoadPage/>}/>
            </Routes>
        </Router>
    </React.StrictMode>,
)
