import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [code, setCode] = useState('');
  const [step, setStep] = useState(1);
  const [timeLeft, setTimeLeft] = useState(120); // 120 soniyaga teskari sanash (2 daqiqa)
  const asosiy_link = "https://api.projectsplatform.uz";
  const navigate = useNavigate();

  useEffect(() => {
    if (step === 2 && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [step, timeLeft]);

  useEffect(() => {
    if (timeLeft === 0) {
      handleTimerEnd();
    }
  }, [timeLeft]);

  const handleTimerEnd = () => {
    alert("Vaqt tugadi. Qayta kod yuboring.");
    setStep(1);
    setTimeLeft(120);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    const loading = document.getElementById("loading");
    loading && loading.classList.remove("hidden");
    try {
      const response = await axios.post(`${asosiy_link}/accounts/login`, {
        username,
        password
      });
      if (response?.data) {
        if(response.data.is_active){
          setStep(2);
          console.log(response?.data);
        } else {
          const url_link = response.data.url;
          
          navigate('/activation', { state: { activationLink: url_link } });
        }
      } else {
        const loginError = document.getElementById("login_xatoligi");
        loginError && loginError.classList.remove("hidden");
      }
    } catch (error) {
      const loginError = document.getElementById("login_xatoligi");
      loginError && loginError.classList.remove("hidden");
      console.log("Login xatosi:", error);
    } finally {
      loading && loading.classList.add("hidden");
    }
  };

  const handleCheckCode = async (e) => {
    e.preventDefault();
    const loading = document.getElementById("loading");
    loading && loading.classList.remove("hidden");
    try {
      const response = await axios.post(`${asosiy_link}/accounts/check-login-code`, {
        username,
        password,
        code
      });
      if (response?.data) {
        // Tokenni localStorage’da saqlash
        localStorage.setItem("authToken", response.data.token);
        window.location.href = '/dashboard';
      } else {
        const checkError = document.getElementById("login_check_xatoligi");
        checkError && checkError.classList.remove("hidden");
      }
    } catch (error) {
      const checkError = document.getElementById("login_check_xatoligi");
      checkError && checkError.classList.remove("hidden");
      setCode("");
      console.log("Kod tekshirish xatosi:", error);
    } finally {
      loading && loading.classList.add("hidden");
    }
  };

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    const timerLabel = document.getElementById("timer_label");
    if (seconds <= 20 && timerLabel) {
      timerLabel.style.color = "red";
    }
    return `${minutes}:${remainingSeconds < 10 ? `0${remainingSeconds}` : remainingSeconds}`;
  };

  return (
    <div id="login_page">
      {step === 1 ? (
        <form onSubmit={handleLogin}>
          <h2>KIRISH</h2>
          <p id="login_xatoligi" className="hidden" style={{fontSize: '14px', textAlign: "center", color: "red"}}>
            Username yoki parol xato
          </p>
          <div>
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label>Parol</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <Link to="/reset-password" className="parol_esdan_chiqdi">Parolingiz esingizdan chiqdimi?</Link>
          <button type="submit">Login</button>
          <hr />
          <div style={{display: "inline-flex"}}>
              <p>Hali saytda ro'yxatdan o'tmadingizmi?</p>
              <div style={{width: 20}}></div>
              <Link to="../register" id="loginbutton">Ro'yxatdan o'tish</Link>
          </div>
        </form>
      ) : (
        <form onSubmit={handleCheckCode}>
          <h2>Kodni Tasdiqlash</h2>
          <div>
            <p id="login_check_xatoligi" className="hidden" style={{fontSize: '14px', textAlign: "center", color: "red"}}>
              Kod xato kiritildi
            </p>
            <p style={{fontSize: '16px', marginTop: '5px'}}>
              Kiritish vaqti: <strong id="timer_label">{formatTime(timeLeft)}</strong>
            </p>
            <label>Kod:</label>
            <input
              type="number"
              id="code_input"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </div>
          <button type="submit">Tasdiqlash</button>
        </form>
      )}
    </div>
  );
}

export default Login;
