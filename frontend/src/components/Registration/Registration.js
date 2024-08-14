import './style.css';

const Registration = () => {
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
                        />
                    </div>

                    <div className='inputContainer'>
                        
                        <input className='input' type='email' placeholder='Email' />
                    </div>

                    <div className='inputContainer'>
                        
                        <input
                            className='input'
                            type='password' 
                            autocomplete="current-password" 
                            placeholder='Password'
                            minlength="4"
                            maxlength="12"
                            size="16"
                        />
                    </div>
                    <input className='registrationBtn' type="submit" value="Sign Up" />
                </form>
            </div>
        </>
    );
}
 
export default Registration;