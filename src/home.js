import ProductsKundalikCom from './templates/products.png';
import './card.css';
import { useNavigate } from 'react-router-dom';

function Home() {

  const navigate = useNavigate();

  // kundalikcom ga o'tish
  const handleMoreInfoClick = () => {
    navigate('/kundalikcom'); // /kundalikcom sahifasiga o'tish
  };

  // register ga o'tish
  const handleRegisterClick = () => {
    navigate('/register'); // /register sahifasiga o'tish
  };


  return (
    <div className="home-container">
    <div id="tg_bog" style={{ position: 'fixed', bottom: '60px', right: '30px', zIndex: 1000, display: "inline-flex", justifyItems: "end"}}>
      <div id="block_click"></div>
      <div style={{ position: 'absolyut', bottom: '0', right: '0', zIndex: 2, display: "inline-flex"}}>
        <a href="https://t.me/KundalikCom_avto_login1" target="_blank" rel="noopener noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.287 5.906q-1.168.486-4.666 2.01-.567.225-.595.442c-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294q.39.01.868-.32 3.269-2.206 3.374-2.23c.05-.012.12-.026.166.016s.042.12.037.141c-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8 8 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629q.14.092.27.187c.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.4 1.4 0 0 0-.013-.315.34.34 0 0 0-.114-.217.53.53 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09"/>
        </svg>
        </a>
        <h3> Amonov Dilmurod </h3>
      </div>
      <div style={{ position: 'absolyut', top: '0', right: '0', zIndex: 1, display: "inline-flex"}}>
        <a href="https://t.me/KundalikCom_avto_login2" target="_blank" rel="noopener noreferrer">
        <svg xmlns="http://www.w3.org/2000/svg" width="60" height="60" fill="currentColor" class="bi bi-telegram" viewBox="0 0 16 16">
          <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0M8.287 5.906q-1.168.486-4.666 2.01-.567.225-.595.442c-.03.243.275.339.69.47l.175.055c.408.133.958.288 1.243.294q.39.01.868-.32 3.269-2.206 3.374-2.23c.05-.012.12-.026.166.016s.042.12.037.141c-.03.129-1.227 1.241-1.846 1.817-.193.18-.33.307-.358.336a8 8 0 0 1-.188.186c-.38.366-.664.64.015 1.088.327.216.589.393.85.571.284.194.568.387.936.629q.14.092.27.187c.331.236.63.448.997.414.214-.02.435-.22.547-.82.265-1.417.786-4.486.906-5.751a1.4 1.4 0 0 0-.013-.315.34.34 0 0 0-.114-.217.53.53 0 0 0-.31-.093c-.3.005-.763.166-2.984 1.09"/>
        </svg>
        </a>
        <h3>Bexruz Boynazarov </h3>
      </div>
    </div>


      {/* Product Card */}
      <div className="product-card">
        <div className="product-content">
          <h1 className="product-title">
            KundalikCOM bilan maktabingiz reytingini oshiring! 🎓📈
          </h1>
          <p className="product-description">
            Raqamli asrda barcha sohalarda osonlik va qulayliklar yaratuvchi platformamizni sinab ko'ring.
            Ayni damda bizning KundalikCOM auto login xizmati mavjud!
          </p>
          <div className="product-buttons">
            <button className="product-button" onClick={handleRegisterClick}>
              Hoziroq Bepul Boshlash
            </button>
            <button className="product-button more-info-button" onClick={handleMoreInfoClick}>Batafsil</button>
          </div>
        </div>
        <div className="product-image">
          <img src={ProductsKundalikCom} alt="Product" />
          <div id="home_card">
            <a href='/login'> Kirish</a>
            <a href='/register'>Ro'yxatdan o'tish</a>
          </div>
        </div>
      </div>
      {/* Register Video Card */}
      <div className="video-card" style={{
        width: "100%",
        boxSizing: "border-box",
        padding: "30px 20%",
        backgroundColor: "rgb(0,100,250, 0.8)",
        borderRadius: "0",
      }}>
        <div className="video-left">
          <div className="video-container">
            <iframe
              src="https://www.youtube.com/embed/dmwgPT86xp4" // Replace with your mobile video ID
              title="Mobile Application Video"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
        <div className="video-content">
          <h2 className="video-title" style={{color: "white"}}>Tizimda ro'yxatdan o'tish uchun qo'llanma</h2>
        </div>
      </div>
      {/* Mobile Video Card */}
      <div className="video-card">
        <div className="video-left">
          <div className="video-container">
            <iframe
              src="https://www.youtube.com/embed/3aSlUPPeupU" // Replace with your mobile video ID
              title="Mobile Application Video"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
        <div className="video-content">
          <h2 className="video-title">
          📱 Mobile dasturni telefonga o'rnatish va undan foydalanish uchun qo'llanma</h2>
        </div>
      </div>

      {/* Desktop Video Card */}
      <div className="video-card">
        <div className="video-content">
          <h2 className="video-title">
          💻 Desktop dasturimizdan to'liq foydalanish haqida videoni tomosha qiling
          </h2>
        </div>
        <div className="video-right">
          <div className="video-container">
            <iframe
              src="https://www.youtube.com/embed/6c1mbNZEHfs" // Replace with your desktop video ID
              title="Desktop Application Video"
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
