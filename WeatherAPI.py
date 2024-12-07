import requests
import tkinter as tk
from tkinter import Canvas, PhotoImage
from PIL import Image, ImageTk
import io

# Function to get the weather data from the API
def get_weather_data():
    url = "http://api.weatherstack.com/current?access_key=468b7a347ea89edcfc7aad284a014208"
    querystring = {"query":"Sheffield, United Kingdom"}
    try:
        response = requests.get(url, params=querystring)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Function to calculate the color based on temperature
def calculate_color(temp):
    # Normalize the temperature to a range of 0 to 1
    normalized_temp = min(max(temp, 0), 50) / 50.0
    # Calculate the red and blue components
    red = int(normalized_temp * 255)
    blue = int((1 - normalized_temp) * 255)
    return f'#{red:02x}00{blue:02x}'

# Function to update the circle color based on temperature
def update_circle():
    weather_data = get_weather_data()
    if weather_data:
        temp = weather_data['current']['temperature']
        windspeed = weather_data['current']['wind_speed']
        icon_url = weather_data['current']['weather_icons'][0]
        color = calculate_color(temp)
        canvas.itemconfig(circle, fill=color)
        temp_label.config(text=f"Temperature: {temp}°C")
        wind_label.config(text=f"Wind Speed: {windspeed} km/h")
        
        # Fetch and display the weather icon
        icon_response = requests.get(icon_url)
        icon_image = Image.open(io.BytesIO(icon_response.content))
        icon_photo = ImageTk.PhotoImage(icon_image)
        image_label.config(image=icon_photo)
        image_label.image = icon_photo  # Keep a reference to avoid garbage collection

    root.after(60000, update_circle)  # Update every 60 seconds

# Create the main window
root = tk.Tk()
root.title("Weather Temperature Circle")

# Create a canvas to draw the circle
canvas = Canvas(root, width=200, height=200)
canvas.pack()

# Draw the circle
circle = canvas.create_oval(50, 50, 150, 150, fill='blue')

# Create a label to display the temperature
temp_label = tk.Label(root, text="Temperature: --°C")
temp_label.pack()

# Create a label to display the wind speed
wind_label = tk.Label(root, text="Wind Speed: -- km/h")
wind_label.pack()

# Create a label to display the weather icon
image_label = tk.Label(root)
image_label.pack()

# Update the circle color initially
update_circle()

# Start the Tkinter event loop
root.mainloop()