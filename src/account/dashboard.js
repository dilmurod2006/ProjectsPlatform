import './dashboard.css'; // Stil uchun CSS fayl
import React, { useState, useEffect } from 'react';
import { Link, Outlet, useNavigate } from 'react-router-dom'; // useNavigate import qilish
import axios from 'axios';


const show_panel = () => {
  var button = document.getElementById("menyu-toggle-button");
  var menyu_panel = document.getElementById("menu-bar");
  var menyu_panel_content = document.getElementById("menu-bar-content");
  if (button) {
    button.style.display = "none"; // Hide the button if it exists
  }
  if (menyu_panel) {
    menyu_panel.style.display = "flex"; // Hide the menyu_panel if it exists
  }
  if(menyu_panel_content){
    menyu_panel_content.style.transform = "translateX(0)"
  }
}
const close_panel = () => {
  var button = document.getElementById("menyu-toggle-button");
  var menyu_panel = document.getElementById("menu-bar");
  console.log(window.width);
  if (window.innerWidth < 810){
    if (button) {
      button.style.display = "flex"; // Hide the button if it exists
    }
    if (menyu_panel) {
      menyu_panel.style.display = "none"; // Hide the menyu_panel if it exists
    }
  }
}

const Dashboard = () => {
  const [menyuPage, setMenyuPage] = useState(1);
  const [fullName, setFullName] = useState('');
  const [balance, setBalance] = useState(0);
  const token = localStorage.getItem('authToken'); // Tokenni olish
  const navigate = useNavigate(); // useNavigate hookini chaqirish

  useEffect(() => {
    // Agar token bo'lmasa, login sahifasiga yo'naltirish
    if (!token) {
      window.location.href = '/login';
      return;
    }

    const fetchUserData = async () => {
      try {
        const response = await axios.post(
          'https://api.projectsplatform.uz/accounts/about_account',
          { token }
        );
        setFullName(response.data.full_name);
        setBalance(response.data.balance);
      } catch (error) {
        console.error('Foydalanuvchi ma\'lumotlarini olishda xato:', error);
        // Agar user ma'lumotlari olishda xato bo'lsa, login sahifasiga yo'naltirish
        window.location.reload();
      }
    };

    fetchUserData();
  }, [token, navigate]);

  const handleLogout = () => {
    // Local storage'dan authToken o'chirish
    localStorage.removeItem('authToken');
    // Foydalanuvchini bosh sahifaga yo'naltirish
    window.location.href = "/";
  };

  return (
    <div className="dashboard">
      {/* Menu Bar */}
      <aside id="menu-bar" className='hide'>
        <button id="menyu-close-button" onClick={close_panel}>
        </button>
        <div id="menu-bar-content">
          <ul>
            <h2>Menu</h2>
            <li><Link to="/dashboard/kundalikcom" onClick={close_panel}><i className="icon-dashboard">📋 </i>KundalikCOM</Link></li>
            <li><Link to="/dashboard/xarajatlar" onClick={close_panel}><i className="icon-expenses">💸 </i>Xarajatlar</Link></li>
            <li><Link to="/dashboard/sozlamalar" onClick={close_panel}><i className="icon-settings">⚙️ </i>Sozlamalar</Link></li>
          </ul>
          <button id="logout" onClick={handleLogout}>
            <span>Chiqish</span>
            <i className="icon-logout">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <g>
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <path d="M12 16l4-4-4-4" stroke="currentColor" strokeWidth="2" fill="none"/>
                  <path d="M8 12H16" stroke="currentColor" strokeWidth="2" fill="none"/>
                </g>
              </svg>
            </i>
          </button>
        </div>
      </aside>

      {/* Dashboard qismi */}
      <div className="dashboard-content">
        {/* Header */}
        <header className="dashboard-header">
          <div className="welcome">
            <button id="menyu-toggle-button" onClick={show_panel}>≡</button>
          </div>
          <div className="welcome">
            Balance: <strong>{Intl.NumberFormat('uz-UZ', { style: 'decimal' }).format(balance)}</strong> so'm
          </div>
          <div className="account">
            <span>{fullName}</span>
            <strong className="icon-account">👤</strong>
          </div>
        </header>

        {/* Kontent qismi */}
        <main className="main-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Dashboard;
