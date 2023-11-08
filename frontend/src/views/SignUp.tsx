import React, { FC, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { useNavigate } from 'react-router';

import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import { signUp, isAuthenticated } from '../utils/auth';
import { Alert } from '@mui/material';

const defaultTheme = createTheme();

export const SignUp: FC = () => {
    const navigate = useNavigate();

    const [error, setError] = useState<string>('');

    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const email = data.get('email')?.toString()
        const pwd = data.get('password')?.toString()
        const pwd_confirmation = data.get('password confirmation')?.toString()

        if (pwd !== pwd_confirmation) setError('Passwords do not match');
        else {
            setError('');
            try {
                if (email && pwd && pwd_confirmation){
                    const data = await signUp(email, pwd, pwd_confirmation);
                }
                if (data) navigate('/');
            } catch (err) {
                if (err instanceof Error) {
                        // handle errors thrown from frontend
                        setError(err.message);
                    } else {
                        // handle errors thrown from backend
                        setError(String(err));
                    }
            }
        }
    };        

    return isAuthenticated() ? (
        <Navigate to="/" />
    ) : (
        <ThemeProvider theme={defaultTheme}>
            <Container component="main" maxWidth="xs">
                <CssBaseline />
                <Box
                    sx={{
                        marginTop: 8,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                }} >
                    <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                        <LockOutlinedIcon />
                    </Avatar>
                    <Typography component="h1" variant="h5">
                        Sign up
                    </Typography>
                    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
                        <Grid container spacing={2}>
                            {/* <Grid item xs={12} sm={6}>
                                <TextField
                                autoComplete="given-name"
                                name="firstName"
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                autoFocus
                                />
                            </Grid> */}
                            {/* <Grid item xs={12} sm={6}>
                                <TextField
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
                                />
                            </Grid> */}
                            <Grid item xs={12}>
                                <TextField
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="new-password"
                                />
                            </Grid>
                            <Grid item xs={12}>
                                <TextField
                                required
                                fullWidth
                                name="password confirmation"
                                label="Password confirmation"
                                type="password"
                                id="password_confirmation"
                                />
                            </Grid>
                        </Grid>
                        <Grid sx={{mt: 3}}>
                            {error && (
                                <Grid item>
                                    <Alert severity='error'>{error}</Alert>
                                </Grid>
                            )}
                        </Grid>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Sign Up
                        </Button>
                        <Grid container justifyContent="flex-end">
                            <Grid item>
                                <Link href="#" variant="body2">
                                    Already have an account? Sign in
                                </Link>
                            </Grid>
                        </Grid>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
};
