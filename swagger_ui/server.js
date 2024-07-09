const express = require('express');
const swaggerUi = require('swagger-ui-express');
const YAML = require('yamljs');
const { createProxyMiddleware } = require('http-proxy-middleware');
const cors = require('cors');

const app = express();
const swaggerDocument = YAML.load('./openapi.yaml');

// Cấu hình CORS
app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middleware để parse JSON và form data
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Cấu hình Swagger UI
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// Xử lý yêu cầu OPTIONS
app.options('*', cors());

// Proxy middleware để chuyển tiếp yêu cầu đến Odoo server
const odooProxy = createProxyMiddleware({
  target: 'http://localhost:8069',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '',
  },
  onProxyReq: (proxyReq, req, res) => {
    if (req.headers.cookie) {
      proxyReq.setHeader('Cookie', req.headers.cookie);
    }
  },
});

// Áp dụng proxy cho các route /api và /web
app.use(['/api', '/web'], odooProxy);

// Route đăng nhập
app.post('/web/session/authenticate', async (req, res, next) => {
  console.log('Received authentication request');
  // Chuyển tiếp yêu cầu đến Odoo server thông qua proxy
  odooProxy(req, res, next);
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log(`Swagger UI is available at http://localhost:${PORT}/api-docs`);
});
