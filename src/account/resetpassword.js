import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function ResetPassword() {
  const [username, setUsername] = useState('');
  const [reset_code, setCode] = useState('');
  const [password, setNewPassword] = useState('');
  const [step, setStep] = useState(1);

  const handleRequestCode = async (e) => {
    e.preventDefault();
    const loading = document.getElementById("loading");
    try{loading.classList.remove("hidden")}catch{}
    try {
      const response = await axios.post('https://api.projectsplatform.uz/accounts/reset-password-request', {
        username
      });

      if (response.data) {
        setStep(2);
      }
    } catch (error) {
      window.location.reload();
      console.error('Kod yuborishda xatolik');
      alert('Username xato yoki tizimda mavjud emas.');
    }
    loading.classList.add("hidden")
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    const loading = document.getElementById("loading");
    try{loading.classList.remove("hidden")}catch{}
    try {
      const response = await axios.post('https://api.projectsplatform.uz/accounts/reset-password', {
        username,
        password,
        reset_code
      });

      if (response.data) {
        window.location.href = '/login';
      }
    } catch (error) {
      window.location.reload();
      console.error('Parolni yangilashda xatolik');
      alert('Kod yoki yangi parolda xatolik mavjud.');
    }
    loading.classList.add("hidden")
  };

  return (
    <div id="login_page">
      {step === 1 ? (
        <form onSubmit={handleRequestCode}>
          <h2>Parolni Qayta Tiklash</h2>
          <div>
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <button type="submit">Kodni Yuborish</button>
          <Link to="/login" className="ruyxatdan_utish">Kirish sahifasiga qaytish</Link>
        </form>
      ) : (
        <form onSubmit={handleResetPassword}>
          <h2>Yangi Parolni O‘rnatish</h2>
          <div>
            <label>Kod:</label>
            <input
              type="number"
              value={reset_code}
              onChange={(e) => setCode(e.target.value)}
              required
            />
          </div>
          <div>
            <label>Yangi Parol:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit">Parolni Yangilash</button>
        </form>
      )}
    </div>
  );
}

export default ResetPassword;
