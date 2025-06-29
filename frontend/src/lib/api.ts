import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from "axios";

// Configuración base de Axios
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:3001/api",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para requests
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Aquí puedes agregar tokens de autenticación
    const token = localStorage.getItem("authToken");
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Interceptor para responses
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error: AxiosError) => {
    // Manejo de errores global
    if (error.response?.status === 401) {
      // Redirigir a login si no está autenticado
      localStorage.removeItem("authToken");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

// Funciones de API específicas para AsgardStore
export const productAPI = {
  // Obtener productos
  getProducts: (params?: any) => api.get("/products", { params }),

  // Obtener producto por ID
  getProduct: (id: string) => api.get(`/products/${id}`),

  // Obtener categorías
  getCategories: () => api.get("/categories"),

  // Buscar productos
  searchProducts: (query: string) =>
    api.get("/products/search", {
      params: { q: query },
    }),
};

export const authAPI = {
  // Login
  login: (credentials: { email: string; password: string }) =>
    api.post("/auth/login", credentials),

  // Registro
  register: (userData: { email: string; password: string; name: string }) =>
    api.post("/auth/register", userData),

  // Logout
  logout: () => api.post("/auth/logout"),

  // Verificar token
  verifyToken: () => api.get("/auth/verify"),
};

export const orderAPI = {
  // Crear orden
  createOrder: (orderData: any) => api.post("/orders", orderData),

  // Obtener órdenes del usuario
  getUserOrders: () => api.get("/orders/user"),

  // Obtener orden por ID
  getOrder: (id: string) => api.get(`/orders/${id}`),
};

export default api;
