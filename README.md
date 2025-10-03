# **📈 Interactive Crypto Dashboard with Streamlit**

An interactive web application built with Streamlit to visualize and analyze real-time market data for popular cryptocurrencies.

## **Key Features**

* **User-Friendly Interface**: Select your favorite crypto (BTC, ETH, DOGE) from a simple dropdown menu.  
* **Interactive Charts**: Powered by Plotly for dynamic data exploration with hover, zoom, and pan functionalities.  
* **Sliding Timeline**: A built-in rangeslider on the price chart makes it easy to focus on specific time periods over the last 60 days.  
* **Live Data**: Fetches up-to-date market data directly from the CoinGecko API.  
* **Optimized Performance**: Leverages Streamlit's caching to ensure a fast and responsive experience.

## **TechStack**

* **Python**: The core programming language.  
* **Streamlit**: For building the interactive web application.  
* **Pandas**: For data manipulation and processing.  
* **Plotly**: For creating interactive data visualizations.  
* **Requests**: For fetching data from the API.

## **Getting Started**

Follow these steps to get the dashboard running on your local machine.

### **Prerequisites**

* Make sure you have **Python 3.7+** installed on your system.

### **Installation & Setup**

1. **Create a Project Folder**: Make a new folder for this project and save the Python script inside it as `crypto_app.py`.  
2. **Open Your Terminal**: Launch your terminal or command prompt.  
3. **Navigate to Your Project Folder**: Use the cd command to move into the folder you just created.  
   `cd path/to/your/project_folder`

4. **Install Required Libraries**: Run the following command to install all the necessary packages.  
   `pip install streamlit pandas plotly requests`

### **Running the Application**

1. **Execute the Run Command**: While inside your project folder in the terminal, run the following command:  
   `streamlit run crypto_app.py`

2. **View the Dashboard**: A new tab will automatically open in your web browser with the app. If not, navigate to the local URL shown in your terminal (usually `http://localhost:8501`).
