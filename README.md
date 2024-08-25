# Simple Weather Application

This is a Django-based web application that provides weather information for a city or country. Users can search for weather data or get weather data at your location, view forecasts, and subscribe to daily weather updates via email. All API processing is handled on the backend.

## Features
- **Search Weather by City or Country**: Users can search for a city's or country's current weather information including temperature, wind speed, humidity, and more.
- **Weather Forecast**: Displays a 4-day weather forecast. Users can load more to see additional forecast days.
- **Weather History**: Temporarily saves weather information searched by users during the day for quick access in database.
- **Email Subscription**: Users can register and unsubscribe to receive daily weather forecast information via email. A confirmation email is sent to complete the subscription process.
- **Deploy to Live Server**: Instructions to deploy the application live are provided.

## Tech Stack
- **Backend**: Django, Python
- **Frontend**: HTML, CSS, JavaScript (for geolocation)
- **Database**: SQLite
- **APIs**: 'https://www.weatherapi.com'

## Prerequisites
- Python 3.10.7
- pip (Python package manager) in requirements.txt
- Django
- A weather API key (e.g., from [WeatherAPI.com](https://www.weatherapi.com))

## Getting Started

### 1. Create a virtual environment
```bash
python -m venv env
env\Scripts\activate
```

### 2. Clone the repository
```bash
git clone https://github.com/PhungHuuTai/WeatherApp_Django.git
```

### 3. Install dependencies
Install the required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a .env file in the root of your project and add the following:
```
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
API_KEY=your_weather_api_key
API_URL=http://api.weatherapi.com/v1
```
Replace placeholders with your actual configuration values.

### 5. Apply migrations
```bash
python manage.py migrate
```

### 6. Run the server
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ to access the application.


## Usage
- ### 1. Search Weather: Enter a city or country name to view the current weather information and a 4-day forecast.
- ### 2. Load More Forecasts: Click "Load More" to see additional forecast days.
- ### 3. Subscribe to Daily Updates: Enter an email address to subscribe to daily weather forecasts. A confirmation email will be sent to complete the subscription.
- ### 4. Unsubscribe: Option to unsubscribe from daily weather emails.

## Demo
A live demo of the application is available at: ***https://drive.google.com/file/d/1Z_VrI1HoobmW2kJd3pxMZAw0a_N7MVi8/view?usp=sharing***

## Deploy on PythonAnywhere 
### 1.Sign Up or Log In
- Go to PythonAnywhere and sign up for a free account or log in if you already have one.

### 2.Create a New Web App
- Navigate to the Web tab on the PythonAnywhere dashboard.
- Click on Add a new web app.

### 3.Choose Web Framework
- Select the option for a Manual configuration and then select Django when prompted.
- Choose the correct Python version that matches the one used in your development environment.

### 4.Set Up Virtual Environment
- If you accidentally deleted your virtual environment (as mentioned earlier), recreate it using the following commands in your PythonAnywhere Bash console:

```bash
mkvirtualenv myenv --python=/usr/bin/python3.x
```
Replace myenv with your desired virtual environment name and 3.x with your specific Python version.

- Install required packages using:
```bash
pip install -r /home/yourusername/yourprojectname/requirements.txt
```
Make sure to replace /path/to/your/requirements.txt with the actual path.

### 5.Configure WSGI File
- Navigate to the WSGI configuration file on the Web tab (it usually points to yourusername_pythonanywhere_com_wsgi.py).
- Update the WSGI file to point to your Django project settings:
```bash
path = '/home/yourusername/yourprojectname'
if path not in sys.path:
    sys.path.append(path)

project_folder = os.path.expanduser('~/yourprojectname')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'yourprojectname.settings'
```
- Replace yourusername with your PythonAnywhere username and yourprojectname with the name of your Django project.

### 6. Environment Variables:
If your application uses environment variables (like API keys), add them in the Web tab under the Environment variables section.

### 7.Reload Your Web App:
- After making all the configurations, go to the Web tab and click the Reload button for your web application.

## NOW ACCESS MY APPLICATION in: 
***https://huutai.pythonanywhere.com/***
