import React, { useState, useEffect } from "react";
import axios from "axios";
import "./AdminPanel.css"; // CSS faylni import qilish
import { useParams } from 'react-router-dom';

const API_BASE_URL = "https://api.projectsplatform.uz";

function AdminPanel() {
    const { token } = useParams();
    const [stats, setStats] = useState({
        usersCount: "Loading...",
        mobileCount: "Loading...",
        kundalikcomCount: "Loading..."
    });
    const [searchResults, setSearchResults] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [paymentStatus, setPaymentStatus] = useState("");
    const [isPaymentVisible, setPaymentVisible] = useState(false);
    const [tgId, setTgId] = useState('');

    useEffect(() => {
        const tokenFromUrl = token;
        loadStats(tokenFromUrl);
    }, [token]);

    async function fetchData(endpoint) {
        try {
            const response = await axios.get(`${API_BASE_URL}${endpoint}`);
            return response.data;
        } catch (error) {
            console.error("API Error:", error);
            setPaymentStatus("Xatolik yuz berdi.");
            return null;
        }
    }

    async function loadStats(token) {
        const usersData = await fetchData(`/admin/get-users?token=${token}`);
        const mobileData = await fetchData(`/admin/get-mobilekundalikcom?token=${token}`);
        const kundalikcomData = await fetchData(`/admin/get-pckundalikcom?token=${token}`);

        if (usersData && mobileData && kundalikcomData) {
            setStats({
                usersCount: usersData?.users?.length || "Error",
                mobileCount: mobileData?.mobilekundalikcom?.length || "Error",
                kundalikcomCount: kundalikcomData?.pckundalikcom?.length || "Error"
            });
        }
    }

    async function handleSearch(event) {
        event.preventDefault();
        const query = event.target.elements.query.value.trim();
        try {
            const response = await axios.post(`${API_BASE_URL}/admin/find_user`, {
                admin_token: token,
                text: query
            });
            setSearchResults(response.data.users || []);
        } catch (error) {
            console.error("Search Error:", error);
            setSearchResults([]);
        }
    }

    async function handlePaymentSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        formData.append("admin_token", token);
        formData.set("tg_id", tgId);
        console.log(tgId);
        // FormData ni konsolga chop etish
        formData.forEach((value, key) => {
            console.log(key + ": " + value);
        });
        
        try {
            // const response = 
            await axios.post(`${API_BASE_URL}/admin/payment`, formData, {
                headers: { "Content-Type": "multipart/form-data" }
            });
            setPaymentStatus("To'lov muvaffaqiyatli qo'shildi!");
        } catch (error) {
            console.error("Payment Error:", error);
            setPaymentStatus("Xatolik yuz berdi.");
        }
    }

    function showPayment() {
        setPaymentVisible(true);
        setPaymentStatus("");
    }

    function closePayment() {
        setPaymentVisible(false);
    }

    return (
        <div className="container">
            <header className="header">
                <h1>Admin Panel</h1>
            </header>
            <main>
                <section className="stats">
                    <h2>Statistika</h2>
                    <div id="stats-container">
                        <div className="stat-item">
                            <h3>Foydalanuvchilar</h3>
                            <p>{stats.usersCount}</p>
                        </div>
                        <div className="stat-item">
                            <h3>Mobile Foydalanuvchilar</h3>
                            <p>{stats.mobileCount}</p>
                        </div>
                        <div className="stat-item">
                            <h3>KundalikCOM Foydalanuvchilar</h3>
                            <p>{stats.kundalikcomCount}</p>
                        </div>
                    </div>
                </section>

                <section className="search-user">
                    <h2>Foydalanuvchini qidirish</h2>
                    <form onSubmit={handleSearch}>
                        <input type="text" name="query" placeholder="Foydalanuvchi ismi yoki ID" required />
                        <button type="submit">Qidirish</button>
                    </form>
                    <div id="search-results">
                        {searchResults.map(user => (
                            <div
                                className="result-item"
                                key={user.id}
                                onClick={() => {
                                    setSelectedUser(user);
                                    setTgId(user.tg_id);
                                    showPayment();

                                }}
                            >
                                <strong>ID:</strong> {user.id}<br />
                                <strong>Username:</strong> {user.username}<br />
                                <strong>Ism:</strong> {user.full_name}<br />
                                <strong>Balance:</strong> {user.balance} so'm<br />
                                <strong>Email:</strong> {user.email}<br />
                                <strong>Telefon:</strong> {user.phone}<br />
                            </div>
                        ))}
                    </div>
                </section>

                {isPaymentVisible && (
                    <div id="payment-card">
                        <div className="container">
                            {selectedUser && (
                                <section className="payment">
                                    <h2>To'lov qo'shish</h2>
                                    
                                    <strong>ID:</strong> {selectedUser.id}
                                    <h1>{selectedUser.full_name}</h1>
                                    <strong>Balance:</strong> {selectedUser.balance} so'm<br />
                                    <form onSubmit={handlePaymentSubmit}>
                                        <input type="hidden" name="tg_id" value={tgId} id="tg_id" />
                                        <label>
                                            To'lov summasi:
                                            <input type="number" name="tulov_summasi" required />
                                        </label>
                                        <label>
                                            To'lov haqida:
                                            <textarea name="bio" defaultValue="Bizga ishonch bildirganingiz uchun rahmat!" />
                                        </label>
                                        <label>
                                            To'lov tasdig'i (rasm):
                                            <input type="file" name="payment_chek_img" required />
                                        </label>
                                        <button type="submit">Yuborish</button>
                                    </form>
                                    <p>{paymentStatus}</p>
                                </section>
                            )}
                        </div>
                        <button id="payment-page-close" onClick={closePayment}>Yopish</button>
                    </div>
                )}
            </main>
        </div>
    );
}

export default AdminPanel;
