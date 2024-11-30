import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LandingPage from './LandingPage.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<LandingPage/>}/>
            </Routes>
        </Router>
    </React.StrictMode>,
)
