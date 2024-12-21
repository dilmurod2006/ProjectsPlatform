import React from "react";
import './about.css';  // Import the CSS file for styling
import dilmurod_image from "./templates/dilmurod.png";
import bexruz_image from "./templates/bexruz.png";
import testmax_image from "./templates/testmax.png";
import mandat_bot_image from "./templates/mandat_bot.png";
import kundalikcom_image from "./templates/kundalikcom_icon.png";
import youtube_icon from "./templates/youtube.png";
import telegram_image from "./templates/telegram.png";
import { useNavigate } from 'react-router-dom';

const About = () => {

  // test max url ni yo'naltirish
  const navigate = useNavigate();
  const handleTestMaxClick = () => {
    navigate('/testmax'); // "/testmax" yo'nalishga yo'naltirish
  };

  // Mandat bot url ni yo'naltirish
  const handleMandatBotClick = () => {
    navigate('/mandatbot'); // "/mandatbot" yo'nalishga yo'naltirish
  };

  // Kundalikcom url ni yo'naltirish
  const handleKundalikcomClick = () => {
    navigate('/kundalikcom'); // "/kundalikcom" yo'nalishga yo'naltirish
  };

  return (
    <div className="about-container">
      <div className="content-wrapper">
        <h1 className="about-title">Biz Haqimizda</h1>

        {/* Team Members Section */}
        <section className="team-section">
          <h2 className="section-title">Asoschilarimiz</h2>
          <div className="team-members">
            {/* Team Member 1 */}
            <div className="team-member">
              <img src={dilmurod_image} alt="Dilmurod Amonov" className="team-member-img" />
              <div className="team-member-info">
                <h3>Amonov Dilmurod</h3>
                <p>Python Fullstack Dasturchisi</p>
                <a href="https://t.me/Softwere_engineer006" target="_blank" rel="noopener noreferrer">
                  <img src={telegram_image} alt="Telegram Icon" className="contact-icon" />
                </a>
              </div>
            </div>

            {/* Team Member 2 */}
            <div className="team-member">
              <img src={bexruz_image} alt="Bexruz Boynazarov" className="team-member-img" />
              <div className="team-member-info">
                <h3>Boynazarov Bexruz</h3>
                <p>Python Fullstack Dasturchisi</p>
                <a href="https://t.me/bexruzdeveloper" target="_blank" rel="noopener noreferrer">
                  <img src={telegram_image} alt="Telegram Icon" className="contact-icon" />
                </a>
              </div>
            </div>
          </div>
        </section>

        {/* Projects Section */}
        <section className="projects-section">
          <h2 className="section-title">Loyihalarimiz</h2>
          <div className="projects-cards">
            {/* Project 1 */}
            <div className="project-card" onClick={handleTestMaxClick}>
              <img src={testmax_image} alt="TestMax" />
              <div className="card-body">
                <h3>TestMax</h3>
                <p>TestMax — bu onlayn test tizimi, foydalanuvchilar testlarni yaratish va o'tkazish imkoniyatiga ega.</p>
              </div>
            </div>

            {/* Project 2 */}
            <div className="project-card" onClick={handleMandatBotClick}>
              <img src={mandat_bot_image} alt="Mandat Bot" />
              <div className="card-body">
                <h3>Mandat Bot</h3>
                <p>Mandat Bot Telegram orqali davlat xizmatlarini avtomatlashtirish uchun mo'ljallangan.</p>
              </div>
            </div>

            {/* Project 3 */}
            <div className="project-card" onClick={handleKundalikcomClick}>
              <img src={kundalikcom_image} alt="KundalikCom AutoLogin" />
              <div className="card-body">
                <h3>KundalikCom AutoLogin</h3>
                <p>O'quvchilarni baholash va tizimga kirish uchun avtomatik tizim.</p>
              </div>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="contact-section">
          <div className="contact-info">
            <p>Bizning YouTube va Telegram kanallarimizga a'zo bo'ling:</p>
          </div>
          <div className="contact-icons">
            <a href="https://t.me/PyPrime" target="_blank" rel="noopener noreferrer">
              <img src={telegram_image} alt="Telegram Icon" className="contact-icon" />
            </a>
            <a href="https://www.youtube.com/channel/PythonPrime" target="_blank" rel="noopener noreferrer">
              <img src={youtube_icon} alt="YouTube Icon" className="contact-icon" />
            </a>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;
