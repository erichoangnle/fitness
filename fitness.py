from tkinter.messagebox import askyesno, showerror, showinfo
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from tkinter import ttk
import tkinter as tk
import pandas as pd
import re, csv
import os.path

def show():
    """
    Plot progress using matplotlib
    """

    pushup = []
    pullup = []
    squat = []
    deadlift = []
    total = []
    date = []
    method = plot_method.get()

    # Prepare data for plotting
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            pushup.append(int(row[1]))
            pullup.append(int(row[2]))
            squat.append(int(row[3]))
            deadlift.append(int(row[4]))
            total.append(int(row[5]))
            date.append(row[0])

    pushup_and_pullup = [(pushup[i] + pullup[i]) for i in range(len(pushup))]

    # Disable tool-bar on graph
    mpl.rcParams['toolbar'] = 'None'

    # Plot last month data
    if method == 'Last month':
        if len(total) == 0:
            showinfo(title='No data', message='No data to plot at the moment')

        if len(total) < 31:
            for _ in range(31 - len(total)):
                pushup.insert(0, 0)
                pullup.insert(0, 0)
                squat.insert(0, 0)
                deadlift.insert(0, 0)
                total.insert(0, 0)
                pushup_and_pullup.insert(0, 0)

        # Plot data
        bar_width = 0.8
        day = [i for i in range(31)]

        plt.bar(day, total[-31:], bar_width, color='b', label = 'Deadlift')
        plt.bar(day, squat[-31:], bar_width, pushup_and_pullup[-31:], color='g', label='Squat')
        plt.bar(day, pullup[-31:], bar_width, pushup[-31:], color='y', label='Pull-up')
        plt.bar(day, pushup[-31:], bar_width, color='r', label='Push-up')

        # Set graph title and x, y limits
        plt.xlim(0.4, max(day) + 0.6)
        plt.ylim(0, max(total[-31:]) + (0.08 + max(total[-31:])))
        plt.title('Last month')

    elif method == 'Weekly average':
        if len(date) < 14:
            showinfo(title='Not enough data', message='Need at least 2 weeks worth of data to create plot.')
            return
        else:
            # Calculate weekly moving average:
            pushup_weekly_average = pd.Series(pushup).rolling(window=7).mean().iloc[7-1:].tolist()
            pullup_weekly_average = pd.Series(pullup).rolling(window=7).mean().iloc[7-1:].tolist()
            squat_weekly_average = pd.Series(squat).rolling(window=7).mean().iloc[7-1:].tolist()
            deadlift_weekly_average = pd.Series(deadlift).rolling(window=7).mean().iloc[7-1:].tolist()
            total_weekly_average = pd.Series(total).rolling(window=7).mean().iloc[7-1:].tolist()

            # Trim list of date to fit data
            day = [datetime.strptime(d, '%a %m-%d-%y').date() for d in date][3:-3]

            # Plot data
            plt.plot(day, total_weekly_average, label='Total')
            plt.plot(day, pushup_weekly_average, label='Pushup')
            plt.plot(day, pullup_weekly_average, label='Pullup')
            plt.plot(day, squat_weekly_average, label='Squat')
            plt.plot(day, deadlift_weekly_average, label = 'Deadlift')

            # Set graph title and x, y limit
            plt.xlim(min(day), max(day))
            plt.ylim(1, max(total_weekly_average) + ( 0.05 + max(total_weekly_average)))
            plt.xticks(rotation=30)
            plt.title('Weekly average')

    # x and y axis label
    plt.xlabel('Day')
    plt.ylabel('Number of reps')

    # Display plot legend
    plt.legend(loc='upper left')

    # Full-screen graph
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()

    # Display graph
    plt.show()

def delete_entry():
    
    # Read database to list
    lines = []
    with open('database.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            lines.append(row)

    # If database is empty
    if len(lines) == 1:
        showinfo(title='Empty database', message='No entry left to delete')
        return

    # If database is not empty
    else:
        answer = askyesno(title='Delete last entry', message='Are you sure?')
        if answer:
            # remove last item in list
            lines.pop()

            # Write modified list to database
            with open('database.csv', mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for item in lines:
                    writer.writerow(item)

            # Re-render text area
            write_text()

def add_entry():
    
    # Get data from text input field
    try:
        data = progress_entry.get()
        if not data:
            data = '0 0 0 0'
        if not re.match('^-*\d+ -*\d+ -*\d+ -*\d+$', data):
            raise ValueError
    except ValueError:
        showerror(title='Error', message='Invalid progress format.')
        progress_entry.delete(0, 20)
        progress_entry.focus_set()

    # Get date from text input field
    try:
        today = date_entry.get()

        if not re.match('^\d{2}/\d{2}/\d{2}$', today):
            raise ValueError

    except ValueError:
        showerror(title='Error', message='Invalid date format')
        date_entry.delete(0, 20)
        date_entry.focus_set()

    # Format date
    today = datetime.strptime(today, '%m/%d/%y')

    # Create new entry
    data = data.split()
    row = [int(entry) for entry in data]
    row.append(row[0] + row[1] + row[2] + row[3])
    row.insert(0, datetime.strftime(today, '%a %m-%d-%y'))

    # Write new entry to database
    with open('database.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(row)

    write_text()

def add_entry_enter(event):
    add_entry()

def write_text():
    
    pullup = []
    pushup = []
    squat = []
    deadlift = []
    total = []
    st.config(state='normal')
    st.tag_configure('red', foreground='red')

    # If database file does not already exist
    if not os.path.isfile('database.csv'):
        st.insert(tk.INSERT, 'You have no record. Start getting fit today!')
        with open('database.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['date', 'pushup', 'pullup', 'squat', 'deadlift', 'total'])

    # If database file exist
    else:
        entries = []
        with open('database.csv', mode = 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in list(reader):
                entries.append(row)
                pushup.append(int(row[1]))
                pullup.append(int(row[2]))
                squat.append(int(row[3]))
                deadlift.append(int(row[4]))
                total.append(int(row[5]))

        st.delete(1.0, tk.END)

        # Write database to text area
        for row in entries:
            if row[0][:3] == 'Mon':
                st.insert(tk.INSERT, '.\n')
            if int(row[5]) == 0:
                st.insert(tk.INSERT, f'{row[0]} - Pushup: {row[1]}, Pullup: {row[2]}, Squat: {row[3]}, Deadlift: {row[4]} - Total: {row[5]}\n', 'red')
            else:
                st.insert(tk.INSERT, f'{row[0]} - Pushup: {row[1]}, Pullup: {row[2]}, Squat: {row[3]}, Deadlift: {row[4]} - Total: {row[5]}\n')

    # Scroll to the bottom of text area
    st.see('end')
    # Disable editting text area
    st.config(state='disabled')


# Root window
root = tk.Tk()
root.title('Personal Fitness Record')
root.geometry('920x385')
root.resizable(False, False)

# History label frame
label_frame1 = ttk.LabelFrame(root, text='My fitness record')
label_frame1.place(x=20, y=20)

# Text are
st = tk.Text(label_frame1, width=82, height=19)
st.grid(padx=10, pady=10)

# Write database to text area
write_text()

# Database label frame
label_frame2 = ttk.LabelFrame(root, text='Manipulate database')
label_frame2.place(x=710, y=20)

# Add text input for new progress
progress = tk.StringVar()
progress_label = ttk.Label(label_frame2, text='New progress:')
progress_label.grid()
progress_entry = ttk.Entry(label_frame2, textvariable=progress)
progress_entry.focus_set()
progress_entry.bind('<Return>', add_entry_enter)
progress_entry.grid(ipadx=20, ipady=2, padx=5, pady=5)

# Add text input for date
date = tk.StringVar()
date_label = ttk.Label(label_frame2, text='Date (mm/dd/yy):')
date_label.grid()
date_entry = ttk.Entry(label_frame2, textvariable=date)
date_entry.insert(0, f"{datetime.strftime(datetime.now(), '%m/%d/%y')}")
date_entry.bind('<Return>', add_entry_enter)
date_entry.grid(ipadx=20, ipady=2, padx=5, pady=5)

# Add entry button
add_entry_button = ttk.Button(label_frame2, text='Add New Progress', command=add_entry)
add_entry_button.grid(ipadx=30, ipady=5, padx=10, pady=5)

# Delete entry button
delete_entry_button = ttk.Button(label_frame2, text='Delete last entry', command=delete_entry)
delete_entry_button.grid(ipadx=35, ipady=5, padx=10, pady=8)

# Show progress label frame
label_frame3 = ttk.LabelFrame(root, text='Show progress')
label_frame3.place(x=710, y=260)

# Create combobox
selected_method = tk.StringVar()
plot_method = ttk.Combobox(label_frame3, textvariable=selected_method)
plot_method['values'] = ['Last month', 'Weekly average', 'Monthly average']
plot_method['state'] = 'readonly'
plot_method.set('Last month')
plot_method.grid(ipadx=10, ipady=2, padx=5, pady=6)

# Show progress button
show_progress_button = ttk.Button(label_frame3, text='Show progress', command=show)
show_progress_button.grid(ipadx=40, ipady=5, padx=10, pady=8)

root.mainloop()


