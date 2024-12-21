import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import './register.css';

function Register() {
    const [fullName, setFullName] = useState('');
    const [sex, setSex] = useState(true); // true for male, false for female
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [passwordConfirm, setPasswordConfirm] = useState('');
    const navigate = useNavigate();
    const location = useLocation();  // Get URL params
    const ref = new URLSearchParams(location.search).get('ref')??-1;  // Extract 'ref' from URL
    // Asosiy api linki
    const asosiy_link = "https://api.projectsplatform.uz";
    
    const handleRegister = async (e) => {
        e.preventDefault();

        if (password !== passwordConfirm) {
            alert("Parollar mos emas");
            return;
        }
        const CREATE_USER_SECRET_KEY="6651751855:AAHKbRLLG6KoNEO5zdYWJ0BdbwupDBCVIFv01d8_m9rvjCQcPYfAFkv4zl1HVCz58oxvAt8iYCrzq_V_fr6";
        
        try {
            console.log(sex);
            const response = await axios.post(`${asosiy_link}/accounts/create_user`, {
                secret_key: CREATE_USER_SECRET_KEY,
                full_name: fullName,
                sex: sex,
                email: email,
                username: username,
                password: password,
                ref: ref  // Add ref parameter to request
            });

            const activationLink = response.data.activation_link;
            navigate('/activation', { state: { activationLink } });
        } catch (error) {
            alert("Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, qayta urinib ko'ring.");
        }
    };

    return (
        <div id="register_page">
            <form onSubmit={handleRegister}>
                <h1>Ro'yxatdan o'tish</h1>
                <div>
                    <label>To'liq ismingiz</label>
                    <input
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                    />
                </div>
                <div>
                    <label>Jinsingiz</label>
                    <select value={sex} onChange={(e) => setSex(e.target.value === 'true')}>
                        <option value={true}>Erkak</option>
                        <option value={false}>Ayol</option>
                    </select>
                </div>
                <div>
                    <label>Elektron pochta</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>
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
                <div>
                    <label>Parolni qayta kiriting</label>
                    <input
                        type="password"
                        value={passwordConfirm}
                        onChange={(e) => setPasswordConfirm(e.target.value)}
                    />
                </div>
                <button type="submit">Ro'yxatdan o'tish</button>
                <hr></hr>
                <div style={{display: "inline-flex"}}>
                    <p>Sizda allaqachon hisobingiz mavjudmi? </p>
                    <div style={{width: 20}}></div>
                    <Link to={"../login"} id="loginbutton" style={{maxHeight: 20}}>Kirsh</Link>
                </div>
            </form>
        </div>
    );
}

export default Register;
