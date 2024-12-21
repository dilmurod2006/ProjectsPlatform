import React from 'react';
import './kundalikcom.css'; // Link to your CSS file

const KundalikCom = () => {
  return (
    <div className="kundalikcom-container">
      <h1>KundalikCOM Auto Login Service</h1>
      <p>
        Ushbu platforma raqamli asrda barcha sohalarda yengilliklar va qulayliklar yaratish uchun ishlab chiqildi.
        Ayni paytda bizda KundalikCOM auto login xizmatimiz mavjud.
      </p>

      <section className="section">
        <h2>Bu nima uchun xizmat qiladi?</h2>
        <p>
          Ushbu xizmatimiz desktop yani Windows 64x operatsion tizimida ishlovchi kompyuterlar uchun mo'ljallangan dastur hisoblanib,
          maktabning barcha foydalanuvchilarini login parollarini kiritilgan holda ularga tezda login qilib, maktab reytingini oshirish uchun mo'ljallangan.
        </p>
      </section>

      <section className="section">
        <h2>Reytingni qay tarzda ko'taradi?</h2>
        <p>
          Reyting maktabda faoliyat yurutuvchilarning tizimga kunlik kirishlariga asoslanadi.
          Barcha foydalanuvchilar kuniga kamida 1 marta tizimga kirishi talab etiladi. Ammo, ota-onalar va o'quvchilar bunga loqayd qaramoqdalar.
          Bizning xizmatimiz orqali ularni avtomatik ravishda tizimga kiritish orqali reytingni oshirish mumkin.
        </p>
      </section>

      <section className="section">
        <h2>O'quvchilar va ota-onalarni avtomatik login qilish</h2>
        <p>
          Xizmatimiz o'quvchilarni hamda ota-onalarni avtomatik tizimga kiritish imkoniyatini beradi. Ushbu qulay xizmat o'qituvchilarning oson foydalanishi uchun ishlab chiqilgan.
        </p>
      </section>
    </div>
  );
};

export default KundalikCom;
