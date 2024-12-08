import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1/system-info';

const api = {
    // Получение списка компьютеров
    getComputers: async () => {
        const response = await axios.get(`${API_URL}/computers/`);
        return response.data;
    },

    // Получение информации о конкретном компьютере
    getComputer: async (computerId) => {
        const response = await axios.get(`${API_URL}/computers/${computerId}`);
        return response.data;
    },

    // Получение последней системной информации
    getLatestSystemInfo: async (computerId) => {
        const response = await axios.get(`${API_URL}/computers/${computerId}/system-info/latest`);
        return response.data;
    },

    // Получение истории системной информации
    getSystemInfoHistory: async (computerId, skip = 0, limit = 100) => {
        const response = await axios.get(
            `${API_URL}/computers/${computerId}/system-info/history`,
            { params: { skip, limit } }
        );
        return response.data;
    }
};

export default api;
