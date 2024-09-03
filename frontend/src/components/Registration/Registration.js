import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import './style.css';

const Registration = () => {
    const [email, setEmail] = useState('');
    const [username, setName] = useState('');
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

    const handleNameChange = event => {
        setName(event.target.value);
        updateButtonState();
    }

    const handlePasswordChange = event => {
        setPassword(event.target.value);
        updateButtonState();
    }

    const updateButtonState = () => {
        const isFormValid = isValidEmail(email) && username !== '' && password !== '';
        setIsDisabled(!isFormValid);
    }

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://26.15.99.17:8000/v1/register', {
                method: 'post',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({
                    'username': username,
                    'email': email,
                    'password': password
                })
                
            });

            const result = await response.json()

            const token = result.access_token;
            localStorage.setItem('token', token)
            window.location.href = '/main'
        }
        
        catch (error){
            console.error('Ошибка аутентификации:', error);
        }
    };

    useEffect(() => {
        updateButtonState();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [email, username, password]);

    return (
        <>
            <div className='have-account'>
                <p className='text'>Already have an account?</p>
                <Link to="/login" className='link'>Sign In</Link>
            </div>
            

            <div className='Registration'>
                <form className='form' onSubmit={handleSubmit}>
                    <h1 className='title'>Sign Up</h1>
                    <div className='inputContainer'>
                        
                        <input 
                            className='input' 
                            type='text' 
                            placeholder='Name' 
                            maxlength="16"
                            value={username}
                            onChange={handleNameChange}
                        />
                    </div>

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
                        className='registrationBtn'
                        disabled={isDisabled}
                        type="submit"
                        value="Sign Up"
                    />

                </form>
            </div>
        </>
    );
}
 
export default Registration;