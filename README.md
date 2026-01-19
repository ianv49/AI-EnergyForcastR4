# AI-EnergyForcastR4
AI-Driven Predictive Maintenance for Renewable Energy Assets
# AI-Driven Predictive Maintenance for Renewable Energy Assets

This project develops a cross-platform application for predictive maintenance of renewable energy assets (wind turbines, solar panels, inverters, batteries). It uses IoT sensor data, external weather/solar APIs, and AI/ML models to forecast failures and optimize maintenance schedules.

---

## 🚀 Features
- Real-time sensor data ingestion (temperature, humidity, irradiance, wind speed).
- External API integration (OpenWeather, NASA POWER, Tomorrow.io).
- Local PostgreSQL + TimescaleDB storage for time-series data.
- Preprocessing scripts for normalization, cleaning, and interpolation.
- Ready for deployment on Raspberry Pi 4, but fully compatible with Mac and Windows laptops during development.

---

## 🛠️ Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/predictive-maintenance-app.git
cd predictive-maintenance-app
