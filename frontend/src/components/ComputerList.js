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
                            sx={{ 
                                cursor: 'pointer',
                                '&:hover': {
                                    boxShadow: 6,
                                    transform: 'scale(1.02)',
                                    transition: 'all 0.2s ease-in-out'
                                }
                            }}
                            onClick={() => navigate(`/computer/${computer.id}`)}
                        >
                            <CardContent>
                                <Box display="flex" alignItems="center" mb={2}>
                                    <Computer sx={{ mr: 1 }} />
                                    <Typography variant="h6">
                                        {computer.hostname}
                                    </Typography>
                                </Box>
                                <Typography color="textSecondary" gutterBottom>
                                    IP: {computer.ip_address}
                                </Typography>
                                <Typography color="textSecondary" gutterBottom>
                                    MAC: {computer.mac_address}
                                </Typography>
                                <Typography color="textSecondary" gutterBottom>
                                    OS: {computer.os_info}
                                </Typography>
                                <Box display="flex" justifyContent="space-between" alignItems="center" mt={2}>
                                    <Chip
                                        icon={<Memory />}
                                        label={new Date(computer.last_seen).toLocaleString()}
                                        color="primary"
                                        variant="outlined"
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
