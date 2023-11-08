import React, { FC } from 'react';

import { logout } from '../utils/auth';
import { Home } from '.'

export const Logout: FC = () => {
    logout()
    return <Home />;
};