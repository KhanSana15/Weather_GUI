import asyncio
import aiohttp
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox


async def get_weather(location, unit):
    """
    Fetch weather information for a given location from wttr.in asynchronously.
    """
    try:
        # Use wttr.in, a free website for weather information
        unit_param = "F" if unit.lower() == 'f' else "C"
        url = f"https://wttr.in/{location}?format=%l:+%C+%t+%w+%h+%p&u={unit_param}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # Check for successful response
                if response.status == 200:
                    return await response.text()
                else:
                    return "Error: Unable to fetch weather data."
    except Exception as e:
        return f"An error occurred: {e}"


def save_to_file(location, weather_info):
    """Save weather information to a file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{location}_weather.txt"
    with open(filename, "w") as file:
        file.write(f"Weather Information for {location}:\n")
        file.write(weather_info + "\n")
        file.write(f"Data fetched at: {timestamp}\n")
    messagebox.showinfo("Success", f"Weather information saved to {filename}")


async def fetch_weather():
    """Fetch weather information and update GUI."""
    location = location_entry.get().strip()
    unit = unit_combo.get().strip()

    if not location:
        messagebox.showwarning("Input Error", "Please enter a valid location.")
        return

    if unit not in ["Celsius (C)", "Fahrenheit (F)"]:
        messagebox.showwarning("Input Error", "Please select a temperature unit.")
        return

    unit = "C" if "Celsius" in unit else "F"

    fetch_button.config(state=tk.DISABLED)
    status_label.config(text="Fetching weather data, please wait...")
    root.update()

    weather_info = await get_weather(location, unit)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result_text.delete(1.0, tk.END)  
    result_text.insert(tk.END, f"Weather Information for {location}:\n{weather_info}\n")
    result_text.insert(tk.END, f"Data fetched at: {timestamp}\n")

    fetch_button.config(state=tk.NORMAL)
    status_label.config(text="")

    if messagebox.askyesno("Save to File", "Do you want to save this information to a file?"):
        save_to_file(location, weather_info)


def start_fetch_weather():
    """Wrapper to run the fetch_weather coroutine in asyncio."""
    asyncio.run(fetch_weather())

root = tk.Tk()
root.title("Weather App")
root.geometry("500x400")

title_label = tk.Label(root, text="Weather App", font=("Helvetica", 18))
title_label.pack(pady=10)

tk.Label(root, text="Enter Location:").pack()
location_entry = tk.Entry(root, width=30)
location_entry.pack(pady=5)

tk.Label(root, text="Select Temperature Unit:").pack()
unit_combo = ttk.Combobox(root, values=["Celsius (C)", "Fahrenheit (F)"], state="readonly")
unit_combo.set("Celsius (C)")
unit_combo.pack(pady=5)

fetch_button = tk.Button(root, text="Fetch Weather", command=start_fetch_weather, font=("Helvetica", 12))
fetch_button.pack(pady=10)

result_frame = tk.Frame(root)
result_frame.pack(pady=10, fill=tk.BOTH, expand=True)
result_text = tk.Text(result_frame, wrap=tk.WORD, height=10, width=50)
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(result_frame, command=result_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

status_label = tk.Label(root, text="", fg="green", font=("Helvetica", 10))
status_label.pack(pady=5)

root.mainloop()