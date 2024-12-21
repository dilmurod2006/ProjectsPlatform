import React, { useState, useEffect } from 'react';
import './sozlamalar.css'; // CSS faylini qo'shishni unutmang
import axios from 'axios';

const Settings = () => {
  const [userData, setUserData] = useState(null);
  const [lastPassword, setLastPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState(''); // Yangi parolni tasdiqlash inputi
  const [message, setMessage] = useState('');
  const token = localStorage.getItem('authToken'); // Local storage'dan tokenni olish

  useEffect(() => {
    const fetchAccountInfo = async () => {
      try {
        const response = await axios.post('https://api.projectsplatform.uz/accounts/about_account', {
          token: token
        });
        setUserData(response.data);
      } catch (error) {
        console.error('Foydalanuvchi ma\'lumotlarini olishda xato:', error);
      }
    };

    fetchAccountInfo();
  }, [token]);

  const handlePasswordChange = async () => {
    if (!lastPassword || !newPassword || !confirmNewPassword) {
      setMessage('Iltimos, barcha maydonlarni to\'liq to\'ldiring.');
      return;
    }

    if (newPassword !== confirmNewPassword) {
      setMessage('Yangi parollar mos kelmaydi.');
      return;
    }

    try {
        const response = await axios.post(
            `https://api.projectsplatform.uz/accounts/change-password-request?token=${token}`,
            {
              last_password: lastPassword,
              new_password: newPassword
            }
          );
          

      if (response.status === 200) {
        setMessage('Parol muvaffaqiyatli o\'zgartirildi.');
      }
    } catch (error) {
      setMessage('Parolni o\'zgartirishda xato.');
      console.error('Parolni o\'zgartirishda xato:', error);
    }
  };

  if (!userData) {
    return <div>Ma'lumotlar yuklanmoqda...</div>;
  }

  return (
    <div className="Settings">
      <h1>Sozlamalar</h1>

      <div className="user-info">
        <h2>Foydalanuvchi Ma'lumotlari</h2>
        <p><strong>Ism:</strong> {userData.full_name}</p>
        <p><strong>Username:</strong> {userData.username}</p>
        <p><strong>Email:</strong> {userData.email}</p>
        <p><strong>Telefon:</strong> {userData.phone}</p>
      </div>

      <div className="change-password">
        <h2>Parolni O'zgartirish</h2>
        <div>
          <label htmlFor="last-password">Eski Parol:</label>
          <input 
            type="password" 
            id="last-password" 
            value={lastPassword} 
            onChange={(e) => setLastPassword(e.target.value)} 
            placeholder="Eski parolni kiriting" 
          />
        </div>
        <div>
          <label htmlFor="new-password">Yangi Parol:</label>
          <input 
            type="password" 
            id="new-password" 
            value={newPassword} 
            onChange={(e) => setNewPassword(e.target.value)} 
            placeholder="Yangi parolni kiriting" 
          />
        </div>
        <div>
          <label htmlFor="confirm-new-password">Yangi Parolni Tasdiqlash:</label>
          <input 
            type="password" 
            id="confirm-new-password" 
            value={confirmNewPassword} 
            onChange={(e) => setConfirmNewPassword(e.target.value)} 
            placeholder="Yangi parolni tasdiqlang" 
          />
        </div>
        <button onClick={handlePasswordChange}>Parolni O'zgartirish</button>

        {message && <p style={{color: (message === "Parolni o'zgartirishda xato." ? "red": message === "Iltimos, barcha maydonlarni to'liq to'ldiring." ? "orange" : message === "Yangi parollar mos kelmaydi." ? "red": message==="Parol muvaffaqiyatli o'zgartirildi."?"green":"blue")}}>{message}</p>}
      </div>
    </div>
  );
};

export default Settings;
