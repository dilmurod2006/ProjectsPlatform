import React from 'react';
import './kundalikcom.css'; // CSS faylini qo'shishni unutmang

const KundalikCOM = () => {
  return (
    <div className="KundalikCOM">
      <h1>KundalikCOM bilan maktabingiz reytingini oshiring! 🎓📈</h1>
      <p>Raqamli asrda barcha sohalarda osonlik va qulayliklar yaratuvchi platformamizni sinab ko'ring. Ayni damda bizning KundalikCOM auto login xizmati mavjud!</p>
      
      <div className="download-cards">
        {/* Kompyuter uchun card */}
        <div className="download-card">
          <h2>Windows Desktop Dasturini Yuklab Olish</h2>
          <p>Desktop versiyasini hoziroq telegram bot orqali yuklab olib, foydalanishni boshlang!</p>
          <a 
            href="https://t.me/projectsplatformbot?start=download" 
            className="download-button" 
            target="_blank" 
            rel="noopener noreferrer">
            Yuklab olish
          </a>
        </div>

        {/* Mobil uchun card */}
        <div className="download-card">
          <h2>Mobil Ilovani Yuklab Olish</h2>
          <p>Mobil ilovamizni telegram bot orqali yuklab olib, istalgan joyda foydalaning!</p>
          <a 
            href="https://t.me/projectsplatformbot?start=download_mobile" 
            className="download-button" 
            target="_blank" 
            rel="noopener noreferrer">
            Yuklab olish
          </a>
        </div>
      </div>
    </div>
  );
};

export default KundalikCOM;
