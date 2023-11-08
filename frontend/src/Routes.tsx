import React, { FC } from 'react';
import { Routes, Route } from 'react-router-dom';
import { useNavigate } from 'react-router';

import { Home, SignUp, Login, Logout } from './views';
import { Admin } from './admin';

export const MyRoutes: FC = () => {
    const navigate = useNavigate();

    return (
        <Routes>
            <Route path="/admin" element={<Admin />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path='/logout' element={<Logout />} />

            <Route path="/" element={
                <div>
                    <header>
                        <Home />
                    </header>
                </div>
            } />
        </Routes>
    );
};
