import React, { useState } from 'react';
import Login from './Login';
import Register from './Register';
import '../styles/Auth.css';

function AuthPage({ onAuthSuccess }) {
  const [isLogin, setIsLogin] = useState(true);

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div>
      {isLogin ? (
        <>
          <Login onLoginSuccess={onAuthSuccess} />
          <div className="auth-toggle">
            <p>Don't have an account?</p>
            <button onClick={toggleAuthMode}>Register</button>
          </div>
        </>
      ) : (
        <>
          <Register onRegisterSuccess={() => setIsLogin(true)} />
          <div className="auth-toggle">
            <p>Already have an account?</p>
            <button onClick={toggleAuthMode}>Login</button>
          </div>
        </>
      )}
    </div>
  );
}

export default AuthPage; 