import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    CircularProgress,
    Chip
} from '@mui/material';
import { Computer, Memory } from '@mui/icons-material';
import api from '../services/api';

const ComputerList = () => {
    const [computers, setComputers] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchComputers = async () => {
            try {
                const data = await api.getComputers();
                setComputers(data);
            } catch (error) {
                console.error('Error fetching computers:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchComputers();
    }, []);

    const handleComputerClick = (computerId) => {
        navigate(`/computer/${computerId}`);
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box sx={{ flexGrow: 1, p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Мониторинг компьютеров
            </Typography>
            <Grid container spacing={3}>
                {computers.map((computer) => (
                    <Grid item xs={12} sm={6} md={4} key={computer.id}>
                        <Card 
                            onClick={() => handleComputerClick(computer.id)}
                            sx={{ 
                                cursor: 'pointer', 
                                transition: 'transform 0.2s',
                                '&:hover': { 
                                    transform: 'scale(1.05)',
                                    boxShadow: 3 
                                } 
                            }}
                        >
                            <CardContent>
                                <Box display="flex" alignItems="center" mb={2}>
                                    <Computer sx={{ mr: 2, color: 'primary.main' }} />
                                    <Typography variant="h6">{computer.hostname}</Typography>
                                </Box>
                                <Typography variant="body2" color="text.secondary">
                                    IP: {computer.ip_address}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    OS: {computer.os_info}
                                </Typography>
                                <Box display="flex" justifyContent="flex-end" mt={2}>
                                    <Chip 
                                        label="Подробнее" 
                                        color="primary" 
                                        size="small" 
                                    />
                                </Box>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
};

export default ComputerList;
