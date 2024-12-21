import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './activation.css';
import main_icon from '../templates/bot_icon.jpg';


function Activation() {
    const location = useLocation();
    const navigate = useNavigate();
    const activationLink = location.state?.activationLink || '/';
    console.log(activationLink);
    const handleActivation = () => {
        window.location.href = activationLink;
    };

    return (
        <div id="activation_page">
            <div className="activation_card">
                <div className="icon_container">
                    <img
                        src={main_icon} // Example icon URL
                        alt="Telegram Bot Icon"
                        className="telegram_icon"
                    />
                </div>
                <h2>Telegram Botimiz orqali Hisobingizni faolashtiring</h2>
                <p>Faolashtirish uchun quyidagi tugmani bosing:</p>
                <button onClick={handleActivation}>Faolashtirish</button>
                <button onClick={() => navigate('/')}>Orqaga</button>
            </div>
        </div>
    );
}

export default Activation;
