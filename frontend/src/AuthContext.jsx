import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext({ token: null, user: null, login: () => {}, logout: () => {}, getUser: () => null });

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [user, setUser] = useState(() => {
    const data = localStorage.getItem('user');
    return data ? JSON.parse(data) : null;
  });

  const login = (newToken, userInfo) => {
    setToken(newToken);
    setUser(userInfo);
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(userInfo));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const getUser = () => {
    return user;
  };

  return (
    <AuthContext.Provider value={{ token, user, login, logout, getUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
