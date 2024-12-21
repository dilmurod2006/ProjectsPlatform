import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Outlet } from 'react-router-dom';
import Login from './account/login';
import Register from './account/register';
import Dashboard from './account/dashboard';
import ResetPassword from './account/resetpassword.js';
import Home from './home';
import About from './about';
import Activation from './account/activation';
import axios from 'axios';
import main_image from './templates/main.png';
import KundalikCom from './kundalikcom.js';
import './home.css';
import KundalikCOM from './account/dashboard/kundalikcom.js';
import Xarajatlar from './account/dashboard/xarajatlar.js';
import Settings from './account/dashboard/sozlamalar.js';
import AddLogins from './add_logins.js';
import AdminPanel from './adminpanel.js';


// App.js ichida footer qo'shish uchun
function Footer() {
  return (
    <footer style={{ backgroundColor: '#0a3d62', color: '#ffffff', padding: '20px 0', textAlign: 'center' }}>
      <div style={{ marginBottom: '10px' }}>
        <span>© {new Date().getFullYear()} ProjectsPlatform. Barcha huquqlar himoyalangan.</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '20px' }}>
        {/* Telegram Icon */}
        <a
          href="https://t.me/PyPrime"
          target="_blank"
          rel="noopener noreferrer"
          style={{ display: 'inline-block', width: '24px', height: '24px' }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="white" class="bi1 bi-telegram1" viewBox="0 0 16 16">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.287 5.906q-1.168.486-4.666 2.01-.567.225-.595.442c-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294q.39.01.868-.32 3.269-2.206 3.374-2.23c.05-.012.12-.026.166.016s.042.12.037.141c-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8 8 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629q.14.092.27.187c.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.4 1.4 0 0 0-.013-.315.34.34 0 0 0-.114-.217.53.53 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09"/>
        </svg>
        </a>
        {/* YouTube Icon */}
        <a
          href="https://www.youtube.com/@PythonPrime"
          target="_blank"
          rel="noopener noreferrer"
          style={{ display: 'inline-block', width: '24px', height: '24px' }}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="#ffffff"
            width="24px"
            height="24px"
          >
            <path d="M23.498 6.186a2.97 2.97 0 0 0-2.088-2.1C19.859 3.573 12 3.573 12 3.573s-7.859 0-9.41.514a2.97 2.97 0 0 0-2.088 2.1C0 7.736 0 12 0 12s0 4.264.502 5.814a2.97 2.97 0 0 0 2.088 2.1c1.551.514 9.41.514 9.41.514s7.859 0 9.41-.514a2.97 2.97 0 0 0 2.088-2.1C24 16.264 24 12 24 12s0-4.264-.502-5.814zM9.545 15.568v-7.14L16 12l-6.455 3.568z" />
          </svg>
        </a>
      </div>
    </footer>
  );
}



function App() {
  const [isMenuOpen, setMenuOpen] = useState(false);
  const [isUserLoggedIn, setIsUserLoggedIn] = useState(false); // yangi holat

  // Tokenni tekshirish
  useEffect(() => {
    const checkUserToken = async () => {
      const token = localStorage.getItem('authToken'); // Tokenni localStorage'dan olish
      if (token) {
        try {
          const response = await axios.post('https://api.projectsplatform.uz/accounts/about_account', { token });
          if (response.data && response.data.full_name) {
            setIsUserLoggedIn(true); // Foydalanuvchi tizimga kirgan bo'lsa
          }
        } catch (error) {
          console.error('Token bilan foydalanuvchi topilmadi', error);
        }
      }
    };

    checkUserToken();
  }, []);

  const toggleMenu = () => {
    setMenuOpen(!isMenuOpen);
  };


  return (
    <Router>
      {/* Routes */}
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} >
          <Route path="" element={<div>
            <h1>Shaxsiy kabinetga Xush kelibsiz!</h1><h2 style={{color: "grey"}}>Biz bilan barchasi oson</h2>
            <div className="dashboard-buttons">
              {/* Foydalanish */}
              <a href='/dashboard/kundalikcom' className="card">
                <div className="icon">📋</div>
                <span className="text">Foydalanish</span>
              </a>
              {/* Xarajatlar */}
              <a href='/dashboard/xarajatlar' className="card">
                <div className="icon">💸</div>
                <span className="text">Xarajatlar</span>
              </a>
              {/* Sozlamalar */}
              <a href='/dashboard/sozlamalar' className="card">
                <div className="icon">⚙️</div>
                <span className="text">Sozlamalar</span>
              </a>
            </div>
          </div>} />
          <Route path="kundalikcom" element={<KundalikCOM />} />
          <Route path="xarajatlar" element={<Xarajatlar />} />
          <Route path="sozlamalar" element={<Settings />} />
        </Route>

        <Route path="/" element={<div>
          <div id="asosiy_template">
            {/* Navbar */}
            <nav id="asosiy_navbar">
              <div className="navbar-container">
                <Link to="/" className="navbar-logo">
                  <img src={main_image} alt="Logo" />
                  ProjectsPlatform
                </Link>

                {/* Menu Toggle Button */}
                <button className="menu-toggle" onClick={toggleMenu}>
                  {isMenuOpen ? '×' : '≡'}
                </button>

                {/* Navbar Links */}
                <ul className={`navbar-links ${isMenuOpen ? 'show' : ''}`} style={{ margin: "0" }}>
                  <li className="asosiy_navbar_item">
                    <Link to="/" onClick={toggleMenu}>BOSH SAHIFA</Link>
                  </li>
                  <li className="asosiy_navbar_item">
                    <Link to="/about" onClick={toggleMenu}>BIZ HAQIMIZDA</Link>
                  </li>
                  <li className="asosiy_navbar_item">
                    <Link to="/kundalikcom" onClick={toggleMenu}>KundalikCOM</Link>
                  </li>
                  {/* Foydalanuvchi tizimga kirgan bo'lsa, Dashboard tugmasi ko'rsatiladi */}
                  {isUserLoggedIn ? (
                    <li className="register-button">
                      <a href="/dashboard" onClick={toggleMenu}>Dashboard</a>
                    </li>
                  ) : (
                    <li className="register-button">
                      <a href="/register" onClick={toggleMenu}>BEPUL BOSHLASH</a>
                    </li>
                  )}
                </ul>
              </div>
            </nav>
          </div>
          <Outlet />
          
          <Footer /> {/* Footerni oxiriga qo'shish */}
        </div>} >
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/adminpanel/:token" element={<AdminPanel />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/kundalikcom" element={<KundalikCom />} />
          <Route path="/activation" element={<Activation />} />
          <Route path="/maktabga_login_parolni_tanitish/:param" element={<AddLogins />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
