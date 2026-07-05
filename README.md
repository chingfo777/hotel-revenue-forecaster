# 🏨 Hotel Revenue & Occupancy Forecasting Engine

An intelligent, data-driven **Revenue Management System (RMS)** and forecasting engine built with Python, Flask, and Scikit-Learn. The application helps hospitality businesses automate predictive analysis, run yield optimization strategies, and perform dynamic competitive market tracking.

🌐 **Live Web Application URL:** [https://hotel-revenue-forecaster.onrender.com](https://hotel-revenue-forecaster.onrender.com)

---

## 🚀 Core Features

1. **Dual Ingestion Architecture**
   * **Manual Mode:** Accept raw `.csv` and `.xlsx` booking logs directly via browser file upload.
   * **Dynamic Tracking Mode:** Paste any commercial hotel directory or travel search page link (e.g., Booking.com, Choice Hotels) to scrape current pricing data dynamically.

2. **Stealth Web Scraping Pipeline**
   * Employs **Playwright** with custom arguments (`AutomationControlled` bypass flags, user-agent masking, and init scripts) to cleanly navigate around enterprise cloud firewalls.
   * Automatically isolates listing nodes, extracts dynamic currency structures using optimized Regular Expressions, and shapes them into standard operational data frames.

3. **Predictive Machine Learning Engine**
   * Automatically normalizes uploaded/scraped inputs and performs feature engineering (extracting indices for weekends, months, and customer surge peak seasons).
   * Trains a **Random Forest Regressor** ensemble model (300 parallel decision trees) with an 80/20 data split pattern.
   * Outputs live accuracy scoring metrics, including **Mean Absolute Error (MAE)** and the **$R^2$ Variance Score**.
   * Projects a daily baseline occupancy curve for a **90-Day Forward Quarter (Q1)** timeline.

4. **Yield Optimization & Adaptive Pricing**
   * Layers a rule-based algorithm over the machine learning projections to output explicit strategic commands:
     * **$\ge 80\%$ Occupancy:** Yields a **+35% Price Increase** (High Demand Maximization)
     * **$\ge 65\%$ Occupancy:** Yields a **+15% Price Increase** (Above-Average Demand)
     * **$\ge 45\%$ Occupancy:** Yields a **Hold Strategy** (Standard Operations)
     * **$< 45\%$ Occupancy:** Yields a **-15% Room Discount** (Low Demand Stimulation)
   * Computes cumulative forward quarters to gauge flat-rate models against adaptive models, outputting the **Estimated TRevPAR Lift Percentage**.

5. **Modern Fluid UI/UX**
   * Built with responsive, clean styling and fully integrated with **Chart.js** for rendering multiple interactive animated graphics.
   * Features a glassmorphic **loading overlay screen** with a rotating spinner that engages during headless browser initialization and model compilation phases to provide smooth visual feedback.

---

## 🛠️ Tech Stack

* **Backend Engine:** Python 3, Flask, Gunicorn (Production HTTP Server)
* **Data Science & ML:** Pandas, NumPy, Scikit-Learn (Random Forest Regressor)
* **Automation & Extraction:** Playwright (Headless Chromium), BeautifulSoup4, Regular Expressions (`re`)
* **Frontend Delivery:** HTML5, CSS3 (Keyframe Animations), JavaScript (ES6), Chart.js

---

## 🔧 Local Setup Instructions

Follow these instructions to run the application on your local development machine:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/chingfo777/hotel-revenue-forecaster.git](https://github.com/chingfo777/hotel-revenue-forecaster.git)
   cd hotel-revenue-forecaster
