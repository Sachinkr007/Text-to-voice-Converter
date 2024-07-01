import tkinter as tk
import boto3
import os
import sys
from tempfile import gettempdir
from contextlib import closing
from botocore.exceptions import NoCredentialsError, ProfileNotFound

# Function to get text from the text box and synthesize speech
def getText():
    try:
        aws_mag_con = boto3.session.Session(profile_name='demo_user')
        client = aws_mag_con.client(service_name='polly', region_name='eu-central-1')
        
        result = textExample.get("1.0", "end").strip()
        if not result:
            print("Text box is empty")
            return
        
        response = client.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3', Text=result, Engine='neural')
        print(response)
        
        if "AudioStream" in response:
            with closing(response['AudioStream']) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(f"IOError: {error}")
                    return
        else:
            print("Could not find the stream!")
            return
        
        if sys.platform == 'win32':
            os.startfile(output)
        else:
            print(f"Audio saved at {output}")
    
    except ProfileNotFound:
        print("The specified profile could not be found. Please check your AWS credentials and configuration.")
    except NoCredentialsError:
        print("Credentials not available. Please check your AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to clear text from the text box
def clearText():
    textExample.delete("1.0", "end")

# Create the main window
root = tk.Tk()
root.geometry("500x350")
root.title("T2S Converter - Amazon Polly")
root.configure(bg='#e0f7fa')

# Create and style the label
label = tk.Label(root, text="Enter text to convert to speech:", bg='#e0f7fa', font=("Helvetica", 14))
label.pack(pady=10)

# Create a styled text box
textExample = tk.Text(root, height=10, wrap='word', font=("Helvetica", 12), relief='solid', bd=2, bg='#ffffff', fg='#000000')
textExample.pack(padx=10, pady=10, fill='both', expand=True)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg='#e0f7fa')
button_frame.pack(pady=10)

# Create and style the Read button
btnRead = tk.Button(button_frame, text="Read", command=getText, bg='#00796b', fg='#ffffff', font=("Helvetica", 12), relief='raised', bd=3, width=10)
btnRead.pack(side='left', padx=20)

# Create and style the Clear button
btnClear = tk.Button(button_frame, text="Clear", command=clearText, bg='#d32f2f', fg='#ffffff', font=("Helvetica", 12), relief='raised', bd=3, width=10)
btnClear.pack(side='right', padx=20)

# Run the application
root.mainloop()
