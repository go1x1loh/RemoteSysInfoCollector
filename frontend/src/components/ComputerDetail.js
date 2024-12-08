import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
    Box,
    Card,
    CardContent,
    Typography,
    Grid,
    CircularProgress,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';
import api from '../services/api';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const ComputerDetail = () => {
    const { id } = useParams();
    const [computer, setComputer] = useState(null);
    const [systemInfo, setSystemInfo] = useState(null);
    const [systemInfoHistory, setSystemInfoHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [computerData, latestInfo, historyData] = await Promise.all([
                    api.getComputer(id),
                    api.getLatestSystemInfo(id),
                    api.getSystemInfoHistory(id)
                ]);
                setComputer(computerData);
                setSystemInfo(latestInfo);
                setSystemInfoHistory(historyData);
            } catch (error) {
                console.error('Error fetching data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 60000); // Обновление каждую минуту

        return () => clearInterval(interval);
    }, [id]);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
            </Box>
        );
    }

    const chartData = {
        labels: systemInfoHistory.map(info => new Date(info.timestamp).toLocaleTimeString()),
        datasets: [
            {
                label: 'CPU Usage (%)',
                data: systemInfoHistory.map(info => info.cpu_usage),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Memory Usage (%)',
                data: systemInfoHistory.map(info => (info.memory_used / info.memory_total) * 100),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }
        ]
    };

    return (
        <Box sx={{ flexGrow: 1, p: 3 }}>
            <Typography variant="h4" gutterBottom>
                {computer.hostname}
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Системная информация
                            </Typography>
                            <Typography>IP: {computer.ip_address}</Typography>
                            <Typography>MAC: {computer.mac_address}</Typography>
                            <Typography>OS: {computer.os_info}</Typography>
                            <Typography>
                                Последнее обновление: {new Date(computer.last_seen).toLocaleString()}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Текущее состояние
                            </Typography>
                            <Typography>CPU: {systemInfo.cpu_usage}%</Typography>
                            <Typography>
                                Память: {Math.round(systemInfo.memory_used)}/{Math.round(systemInfo.memory_total)} GB
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                График использования ресурсов
                            </Typography>
                            <Line data={chartData} />
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Запущенные процессы
                            </Typography>
                            <TableContainer component={Paper}>
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>PID</TableCell>
                                            <TableCell>Имя</TableCell>
                                            <TableCell>CPU %</TableCell>
                                            <TableCell>Память %</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {systemInfo.running_processes.map((process) => (
                                            <TableRow key={process.pid}>
                                                <TableCell>{process.pid}</TableCell>
                                                <TableCell>{process.name}</TableCell>
                                                <TableCell>{process.cpu_percent}</TableCell>
                                                <TableCell>{process.memory_percent}</TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
};

export default ComputerDetail;
