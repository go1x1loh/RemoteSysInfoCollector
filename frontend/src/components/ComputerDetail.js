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
                console.error('Error fetching computer details:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [id]);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
                <CircularProgress />
            </Box>
        );
    }

    if (!computer) {
        return <Typography variant="h6">Компьютер не найден</Typography>;
    }

    // Prepare data for CPU usage chart
    const cpuChartData = {
        labels: systemInfoHistory.map((_, index) => `Point ${index + 1}`),
        datasets: [{
            label: 'CPU Usage (%)',
            data: systemInfoHistory.map(info => info.cpu_usage),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    };

    // Prepare data for Memory usage chart
    const memoryChartData = {
        labels: systemInfoHistory.map((_, index) => `Point ${index + 1}`),
        datasets: [{
            label: 'Memory Used (GB)',
            data: systemInfoHistory.map(info => info.memory_used),
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.1
        }]
    };

    return (
        <Box sx={{ flexGrow: 1, p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Детали компьютера: {computer.hostname}
            </Typography>

            <Grid container spacing={3}>
                {/* Computer Details Card */}
                <Grid item xs={12} md={4}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" gutterBottom>
                                Информация о компьютере
                            </Typography>
                            <Typography variant="body2">
                                <strong>Hostname:</strong> {computer.hostname}
                            </Typography>
                            <Typography variant="body2">
                                <strong>IP Address:</strong> {computer.ip_address}
                            </Typography>
                            <Typography variant="body2">
                                <strong>MAC Address:</strong> {computer.mac_address}
                            </Typography>
                            <Typography variant="body2">
                                <strong>OS:</strong> {computer.os_info}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Latest System Info Card */}
                {systemInfo && (
                    <Grid item xs={12} md={8}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    Последняя системная информация
                                </Typography>
                                <Grid container spacing={2}>
                                    <Grid item xs={6}>
                                        <Typography variant="body2">
                                            <strong>CPU Usage:</strong> {systemInfo.cpu_usage.toFixed(2)}%
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={6}>
                                        <Typography variant="body2">
                                            <strong>Memory Used:</strong> {systemInfo.memory_used.toFixed(2)} GB / {systemInfo.memory_total.toFixed(2)} GB
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={12}>
                                        <Typography variant="body2">
                                            <strong>Running Processes:</strong> {systemInfo.running_processes.length}
                                        </Typography>
                                    </Grid>
                                </Grid>
                            </CardContent>
                        </Card>
                    </Grid>
                )}

                {/* System Info History Charts */}
                {systemInfoHistory.length > 0 && (
                    <>
                        <Grid item xs={12} md={6}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        История использования CPU
                                    </Typography>
                                    <Line data={cpuChartData} />
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Card>
                                <CardContent>
                                    <Typography variant="h6" gutterBottom>
                                        История использования памяти
                                    </Typography>
                                    <Line data={memoryChartData} />
                                </CardContent>
                            </Card>
                        </Grid>
                    </>
                )}
            </Grid>
        </Box>
    );
};

export default ComputerDetail;
