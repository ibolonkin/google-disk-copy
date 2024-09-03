import { useEffect, useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import './style.css';


const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [isDisabled, setIsDisabled] = useState(false);

    function isValidEmail(email){
        return /^\S+@\S+\.\S+$/.test(email);
    }

    const handleEmailChange = event => {

        const newEmail = event.target.value;
        setEmail(newEmail);
        
        if(!isValidEmail(event.target.value)){
            setError('Invalid Email');
            setIsDisabled(true);
        } else {
            setError(null);
        }
        
        updateButtonState();
    }

    const handlePasswordChange = event => {
        setPassword(event.target.value);
        updateButtonState();
    }

    const updateButtonState = () => {
        const isFormValid = isValidEmail(email) && password !== '';
        setIsDisabled(!isFormValid);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://26.15.99.17:8000/v1/auth', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({'email': email, 'password': password}),
                
            });

            if (response.status !== 200){
                setError('Логин или пароль неверный')
            }
            else{

                const result = await response.json()

                const token = result.access_token;
                localStorage.setItem('token', token)
                window.location.href = '/main'
            }

        }
        
        catch (error){
            console.error('Ошибка аутентификации:', error);
        }
        
    }

    useEffect(() => {
        updateButtonState();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [email, password]);

    return (
        <>

            <div className='have-account'>
                <p className='text'>Don't have an account yet?</p>
                <Link to="/" className='link'>Register</Link>
            </div>

            <div className='Login'> 
                <form className='form' onSubmit={handleSubmit}>
                    <h1 className='title'>Sign In</h1>

                    <div className='inputContainer'>
                        
                        <input 
                            className='input'
                            type='email'
                            placeholder='Email'
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    {error && <p style={{color: 'red'}}>{error}</p>}


                    <div className='inputContainer'>
                        
                        <input
                            className='input'
                            type='password' 
                            autocomplete="current-password" 
                            placeholder='Password'
                            minlength="4"
                            maxlength="12"
                            size="16"
                            value={password}
                            onChange={handlePasswordChange}
                        />
                    </div>
                    <input 
                        className='LoginBtn'
                        disabled={isDisabled}
                        type="submit"
                        value="Sign In"
                    />

                </form>
            </div>
        </>
    );
}
 
export default Login;