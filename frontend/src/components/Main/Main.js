import React, { useState, useEffect } from 'react';


const Main = () => {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('token');

        const fetchData = async () => {
            try {
                const response = await fetch('http://26.15.99.17:8000/v1/me', {headers: {"Authorization": `Bearer ${token}`}})
                const data = await response.json()
                setUserData(data);
            } catch (error) {
                console.error('Ошибка получения данных:', error);
            }
        };
        
        fetchData();
    }, []);
    return (
        <>
            {userData ? (
            <h1>
                Hello, {userData.username}
            </h1>
            ) : (
                <p>Загрузка данных...</p>
            )}
        </>
     );
}
 
export default Main;