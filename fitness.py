from tkinter.messagebox import askyesno, showerror, showinfo
from datetime import datetime, date
import matplotlib.pyplot as plt
import customtkinter as ctk
import matplotlib as mpl
import tkinter as tk
import pandas as pd
import re, csv


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")


def days():

    # Count the days from start day June 10, 2021
    today = date.today()
    start_day = date(2021, 6, 10)
    total_day = (today - start_day).days

    return total_day

def write_text():

    lower = []
    mid = []
    upper = []
    calves = []
    total = []
    st.textbox.config(state='normal')
    st.tag_configure('red', foreground='red')

    # Read batase into list
    entries = []
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in list(reader):
            entries.append(row)
            lower.append(int(row[1]))
            mid.append(int(row[2]))
            upper.append(int(row[3]))
            calves.append(int(row[4]))
            total.append(int(row[5]))

    # Write database to text area       
    for row in entries:
        if row[6][:3] == 'Mon':
            st.insert(tk.INSERT, '.\n')
        if int(row[4]) == 0 and int(row[1] + row[2] + row[3]) == 0:
            st.insert(tk.INSERT, f"(Day {row[0]}) {row[6]}: ({row[1]}, {row[2]}, {row[3]}, {row[4]}) -- Total: {row[5]}\n", 'red')
        else:
            st.insert(tk.INSERT, f"(Day {row[0]}) {row[6]}: ({row[1]}, {row[2]}, {row[3]}, {row[4]}) -- Total: {row[5]}\n")
    
    # Print records
    st.insert(tk.INSERT, "----------------------------------------------------------\n")
    st.insert(tk.INSERT, f"Record: L({max(lower):,}) | M({max(mid):,}) | U({max(upper):,}) | C({max(calves):,}) | Total({max(total):,})")

    # Auto scroll to the end of text area
    st.textbox.see('end')
    st.textbox.config(state='disabled')

def check_record(data):

    lower = set()
    mid = set()
    upper = set()
    calves = set()
    total = set()

    # Convert item in data to integer
    for i in range(6):
        data[i] = int(data[i])

    # Open database and add data to set
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in list(reader)[:-1]:
            lower.add(int(row[1]))
            mid.add(int(row[2]))
            upper.add(int(row[3]))
            calves.add(int(row[4]))
            total.add(int(row[5]))

    record_list = []

    # Check if any record is broken and add achievement(s) to list
    if data[1] > max(lower):
        record_list.append(f"Lower body record broken: last highest {max(lower)} (+{data[1] - max(lower)})")

    if data[2] > max(mid):
        record_list.append(f"Abs record broken: last highest {max(mid)} (+{data[2] - max(mid)})")

    if data[3] > max(upper):
        record_list.append(f"Upper body record broken: last highest {max(upper)} (+{data[3] - max(upper)})")

    if data[4] > max(calves):
        record_list.append(f"Calves record broken: last highest {max(calves)} (+{data[4] - max(calves)})")

    if data[5] > max(total):
        record_list.append(f"Total reps record broken: last highest {max(total)} (+{data[5] - max(total)})")

    # Display achievement(s)
    if record_list:
        for item in record_list:
            showinfo(title='New Record', message=f"{item}")

def add_entry(event):
    
    entry()

def entry():

    # Get progress from text input field
    try:
        data = progress_entry.get()
        if not data:
            data = '0 0 0 0'
        if not re.match("^-*\d+ -*\d+ -*\d+ -*\d+$", data):
            raise ValueError

    except ValueError:
        showerror(title='Error', message='Invalid progress format, please try again.')
        progress_entry.delete(0, 15)
        progress_entry.focus_set()

    # Get date from text input field
    try:
        today = d_entry.get()

        if not re.match("^\d{2}/\d{2}/\d{2}$", today) and today != 'today':
            raise ValueError

    except ValueError:
        showerror(title='Error', message='Invalid date format, please try again.')
        d_entry.delete(0, 15)
        d_entry.focus_set()

    # Check if entry time is today
    if today == 'today':
        today = date.today()
    else:
        today = datetime.strptime(today, '%m/%d/%y').date()

    # How many days since the fitness program start
    total_day = (today - date(2021, 6, 10)).days + 1

    # Read database file into list
    lines = []
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        for line in reader:
            lines.append(line)

    # Update progress values if today already exist in database
    if total_day == int(lines[-1:][0][0]):
        
        data = data.split()
        data.insert(0, total_day)

        # Update number of reps and total reps
        lines[-1:][0][1] = int(lines[-1:][0][1]) + int(data[1])
        lines[-1:][0][2] = int(lines[-1:][0][2]) + int(data[2])
        lines[-1:][0][3] = int(lines[-1:][0][3]) + int(data[3])
        lines[-1:][0][4] = int(lines[-1:][0][4]) + int(data[4])
        lines[-1:][0][5] = lines[-1:][0][1] + lines[-1:][0][2] + lines[-1:][0][3]

        # Write update to database
        with open('database.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for line in lines:
                writer.writerow(line)

        write_text()
        check_record(lines[-1:][0])

    # Add new entry to database if today's entry doesn't exist
    else:
        
        # Create new entry
        data = data.split()
        data.insert(0, total_day)
        row = [int(entry) for entry in data]
        row.append(row[1] + row[2] + row[3])
        row.append(datetime.strftime(today, '%a %m-%d-%y'))

        # Write new entry to database
        with open('database.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(row)

        write_text()
        check_record(row)
        
def delete_entry():

    answer = askyesno(title='Delete database', message='Are you sure you want to delete last entry?')
    
    # Delete last entry from database
    if answer:

        # Read database to list
        lines = []
        with open('database.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                lines.append(row)

        # Remove last item in list
        lines.pop()

        # Write modified list to database
        with open('database.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in lines:
                writer.writerow(item)

        # Re-render scrolled text field
        write_text()

def show():

    lower = []
    mid = []
    upper = []
    calves = []
    total = []
    date = []
    method = plot_method.get()

    # Open database and read progress data for plotting
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            lower.append(int(row[1]))
            mid.append(int(row[2]))
            upper.append(int(row[3]))
            calves.append(int(row[4]))
            total.append(int(row[5]))
            date.append(row[6])

    # Disable tool bar on graph
    mpl.rcParams['toolbar'] = 'None'
    
    # Plot last month data
    if method == 'Last month':
        
        # Plot data
        bar_width = 0.8
        day = [i for i in range(31)]

        plt.bar(day, total[-31:], bar_width, 0, color = 'b', label='Upper')
        plt.bar(day, mid[-31:], bar_width, lower[-31:], color = 'y', label='Mid')
        plt.bar(day, lower[-31:], bar_width, color = 'r', label='Lower')

        # Set title for the graph and limit for x and y
        plt.xlim(0.4, max(day) + 0.6)
        plt.ylim(0, max(total[-31:]) + (0.08 * max(total[-31:])))
        plt.title('Last Month')

    # Plot last 2 weeks data
    elif method == 'Calves':
        
        # PLot data
        day = [i for i in range(30)]
        plt.bar(day, calves[-30:], label='Calves')

        # Set title for the graph and limit for x and y
        plt.xlim(0.4, max(day) + 0.6)
        plt.ylim(0, max(calves[-30:]) + (0.05 * max(calves[-30:])))
        plt.title('Calves workout last month')

    # Plot weekly moving average for all data in database
    elif method == 'Weekly average':

        # Calculate weekkly moving average and add values to list
        lower_weekly_average = pd.Series(lower).rolling(window=7).mean().iloc[7-1:].tolist()
        mid_weekly_average = pd.Series(mid).rolling(window=7).mean().iloc[7-1:].tolist()
        upper_weekly_average = pd.Series(upper).rolling(window=7).mean().iloc[7-1:].tolist()
        total_weekly_average = pd.Series(total).rolling(window=7).mean().iloc[7-1:].tolist()

        # Trim the list of date to fit data
        day = [datetime.strptime(d, '%a %m-%d-%y').date() for d in date]
        day = day[3:]
        for _ in range(3):
            day.pop()

        # Plot data
        plt.plot(day, total_weekly_average, label='Total')
        plt.plot(day, lower_weekly_average, label='Lower')
        plt.plot(day, mid_weekly_average, label='Mid')
        plt.plot(day, upper_weekly_average, label='Upper')

        # Set title for the graph and set limit for x and y
        plt.xlim(min(day), max(day))
        plt.ylim(1, max(total_weekly_average) + (0.05 * max(total_weekly_average)))
        plt.xticks(rotation=30)
        plt.title('Weekly Moving Average')

    # Plot monthly moving average for all data in database
    else:

        # Calculate monthly moving average and add values to list
        lower_monthly_average = pd.Series(lower).rolling(window=31).mean().iloc[31-1:].tolist()
        mid_monthly_average = pd.Series(mid).rolling(window=31).mean().iloc[31-1:].tolist()
        upper_monthly_average = pd.Series(upper).rolling(window=31).mean().iloc[31-1:].tolist()
        total_monthly_average = pd.Series(total).rolling(window=31).mean().iloc[31-1:].tolist()

        # Trim list of date to fit data
        day = [datetime.strptime(d, '%a %m-%d-%y').date() for d in date]
        day = day[15:]
        for _ in range(15):
            day.pop()

        # Plot data
        plt.plot(day, total_monthly_average, label='Total')
        plt.plot(day, lower_monthly_average, label='Lower')
        plt.plot(day, mid_monthly_average, label='Mid')
        plt.plot(day, upper_monthly_average, label='Upper')

        # Set title for the graph and set limit for x and y
        plt.xlim(min(day), max(day))
        plt.ylim(1, max(total_monthly_average) + (0.05 * max(total_monthly_average)))
        plt.xticks(rotation=30)
        plt.title('Monthly Moving Average')

    # Graph x and y axis label
    plt.xlabel('Day')
    plt.ylabel('Number of Reps')

    # Display plot legend 
    plt.legend(loc='upper left')

    # Full-screen graph
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    # Display graph
    plt.show()


# Root window
root = ctk.CTk()
root.title("Personal Fitness Record")
root.geometry('730x390')
root.resizable( False, False)

# History label frame
label_frame1 = ctk.CTkFrame(root)
label_frame1.place(x=20, y=20)

# Scrolled text area
st = ctk.CTkTextbox(label_frame1, text_font=('Helvetica', 11), width=460,  height=330)
st.grid(padx=10, pady=10)

# Write database to text area
write_text()

# Database label frame
label_frame2 = ctk.CTkFrame(root)
label_frame2.place(x=510, y=20)

# Add text input for progress
progress_label = ctk.CTkLabel(label_frame2, text='New progress:')
progress_label.grid(padx=5)
progress_entry = ctk.CTkEntry(label_frame2)
progress_entry.focus_set()
progress_entry.bind('<Return>', add_entry)
progress_entry.grid(ipadx=20, ipady=2, padx=5, pady=5)

# Add text input for date
d_label = ctk.CTkLabel(label_frame2, text='Date (mm/dd/yy):')
d_label.grid()
d_entry = ctk.CTkEntry(label_frame2)
d_entry.insert(0, 'today')
d_entry.bind('<Return>', add_entry)
d_entry.grid(ipadx=20, ipady=2, padx=5, pady=5)

# Add entry button
add_entry = ctk.CTkButton(label_frame2, text='Add New Progress', command=entry)
add_entry.grid(ipadx=20, ipady=5, padx=10, pady=5)

# Delete entry button
delete_entry = ctk.CTkButton(label_frame2, text='Delete Last Entry', command=delete_entry)
delete_entry.grid(ipadx=20, ipady=5, padx=10, pady=8)

# Show progress label frame
label_frame3 = ctk.CTkFrame(root)
label_frame3.place(x=510, y=270)

# Create a combobox
plot_method = ctk.CTkComboBox(label_frame3, values=['Calves', 'Last month', 'Weekly average', 'Monthly average'], state='readonly')
plot_method['state'] = 'readonly'
plot_method.set("Last month")
plot_method.grid(ipadx=20, ipady=0, padx=10, pady=9)

# Show progress button
show_progress = ctk.CTkButton(label_frame3, text='Show Progress', command=show)
show_progress.grid(ipadx=20, ipady=5, padx=10, pady=7)

# Start the program
root.mainloop()
