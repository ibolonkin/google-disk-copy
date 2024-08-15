import { useEffect, useState } from 'react';
import './style.css';

const Registration = () => {
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
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
        const isFormValid = isValidEmail(email) && name !== '' && password !== '';
        setIsDisabled(!isFormValid);
    }

    useEffect(() => {
        updateButtonState();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [email, name, password]);

    return (
        <>
            <div className='Registration'>
                <form className='form'>
                    <h1 className='title'>Sign Up</h1>
                    <div className='inputContainer'>
                        
                        <input 
                            className='input' 
                            type='text' 
                            placeholder='Name' 
                            maxlength="16"
                            value={name}
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
                    <input className='registrationBtn' disabled={isDisabled} type="submit" value="Sign Up" />
                </form>
            </div>
        </>
    );
}
 
export default Registration;