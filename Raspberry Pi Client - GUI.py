from tkinter import *
import socket
import os
from tkinter import messagebox
import keyboard
import time
try:
    from website import app
    website = True
except:
    website = False

port = 35491
IP = "anonymous"

class Main:
    def forward(s):
        s.send("forward".encode())
        time.sleep(.050)
        s.send("stop".encode())

    def right(s):
        s.send("right".encode())
        time.sleep(.050)
        s.send("stop".encode())

    def left(s):
        s.send("left".encode())
        time.sleep(.050)
        s.send("stop".encode())

    def backwards(s):
        s.send("backwards".encode())
        time.sleep(.050)
        s.send("stop".encode())

    def stop(s):
        s.send("stop".encode())

    def led(s, color, statues):
        s.send(f"{color} led --{statues}".encode())

    def motor(s, direction):
        if direction == "dance":
            s.send("dance".encode())
            info = messagebox.showinfo("Raspberry Pi Client", "Dancing (ง ͠° ͟ل͜ ͡°)ง")
            exit()
        else:
            s.send(f"{direction}".encode())

    def exit(s):
        s.send("exit".encode())
        s.close()
        exit()

    def autopilot(s, mode, straight_button, circle_button):
        info = messagebox.showinfo("Raspberry Pi Client", "Autopilot mode activated")
        straight_button.destroy()
        circle_button.destroy()
        s.send(f"autopilot --{mode}".encode())

    def autopilot_choice(window, s):
        straight_ap_button = Button(window, text="Straight AP", font=("", 20), command=lambda: Main.autopilot(s, "straight", straight_ap_button, circle_ap_button))
        straight_ap_button.place(relx=0.2, rely=0.3, anchor=N)
        circle_ap_button = Button(window, text="Circle AP", font=("", 20), command=lambda: Main.autopilot(s, "circle", straight_ap_button, circle_ap_button))
        circle_ap_button.place(relx=0.3, rely=0.3, anchor=N)

    def connection_error(window, statues, connect_button):
        connect_button.config(text="Failed", bg="red")
        statues.config(text="A Connection Error Has Occured, Try Again Later")
        window.after(2000, lambda:exit())

    def follow_object(window, s):
        s.send("follow --RGB".encode())
        info = messagebox.showinfo("Raspberry Pi Client", "Follow mode activated, select target in raspberry pi itself")
        window.destroy()

    def website(window, s):
        warning = messagebox.showinfo("Raspberry Pi Client", "If the website didnt open, please make sure you have python3 installed")
        s.send("exit".encode())
        window.destroy()
        os.system("python3 website.py")

    def shutdown(window, s):
        info = messagebox.askyesno("Raspberry Pi Client", "Are you sure you want to shutdown?")
        if info == True:
            s.send("shutdown".encode())
            window.destroy()
            exit()
        else:
            pass

    def security_camera(window, s):
        s.send("security camera".encode())
        info = messagebox.showinfo("Raspberry Pi Client", "Security camera mode activated")
        exit()

    def camera(button1, button2, s):
        s.send("face recognition".encode())
        info = messagebox.showinfo("Raspberry Pi Client", "Face recognition activated")
        button1['state'] = 'disabled'
        button2['state'] = 'disabled'

    def window(window, s):
        print("[+] Connected to server")
        window.destroy()
        window = Tk()
        window.state("zoomed")
        window.title("client")
        window.configure(background="white")

        keyboard.add_hotkey('w', lambda: Main.forward(s)) 
        keyboard.add_hotkey('s', lambda: Main.backwards(s)) 
        keyboard.add_hotkey('d', lambda: Main.right(s)) 
        keyboard.add_hotkey('a', lambda: Main.left(s)) 
        keyboard.add_hotkey(' ', lambda: Main.stop(s)) 

        title = Label(window, text="Raspberry Pi Client", font=("", 60), bg="white")
        title.place(relx=0.26, anchor=N)
        credits = Label(window, text="Coded By Karim", font=("", 20), bg="white")
        credits.place(relx=0.15, rely=0.1, anchor=N)

        forward_button = Button(window, text="  /\  ", font=("", 20), command=lambda: Main.motor(s, "forward"))
        forward_button.place(relx=0.85, rely=0.75, anchor=N)
        backwards_button = Button(window, text="  \/  ", font=("", 20), command=lambda: Main.motor(s, "backwards"))
        backwards_button.place(relx=0.85, rely=0.83, anchor=N)
        right_button = Button(window, text="  >  ", font=("", 20), command=lambda: Main.motor(s, "right"))
        right_button.place(relx=0.91, rely=0.81, anchor=N)
        left_button = Button(window, text="  <  ", font=("", 20), command=lambda: Main.motor(s, "left"))
        left_button.place(relx=0.79, rely=0.81, anchor=N)

        stop_button = Button(window, text="                       STOP                       ", font=("", 20), command=lambda: Main.motor(s, "stop"))
        stop_button.place(relx=0.35, rely=0.9, anchor=N)

        red_led_on_switch = Button(window , text="   ", font=("", 20), bg="red", command=lambda: Main.led(s, "red", "on"))
        red_led_on_switch.place(relx=0.75, rely=0.1, anchor=N)
        red_led_off_switch = Button(window , text="   ", font=("", 20), bg="tomato", command=lambda: Main.led(s, "red", "off"))
        red_led_off_switch.place(relx=0.75, rely=0.2, anchor=N)

        blue_led_on_switch = Button(window , text="   ", font=("", 20), bg="blue", command=lambda: Main.led(s, "blue", "on"))
        blue_led_on_switch.place(relx=0.8, rely=0.1, anchor=N) 
        blue_led_off_switch = Button(window , text="   ", font=("", 20), bg="RoyalBlue1", command=lambda: Main.led(s, "blue", "off"))
        blue_led_off_switch.place(relx=0.8, rely=0.2, anchor=N)

        green_led_on_switch = Button(window , text="   ", font=("", 20), bg="green", command=lambda: Main.led(s, "green", "on"))
        green_led_on_switch.place(relx=0.85, rely=0.1, anchor=N)
        green_led_off_switch = Button(window , text="   ", font=("", 20), bg="SpringGreen2", command=lambda: Main.led(s, "green", "off"))
        green_led_off_switch.place(relx=0.85, rely=0.2, anchor=N)

        front_sensor_distance_text = Label(window, text="Front Sensor Distance: ----cm", font=("", 20), bg="white")
        front_sensor_distance_text.place(relx=0.45, rely=0.45, anchor=N)
        bottom_sensor_distance_text = Label(window, text="Bottom Sensor Distance: ----cm", font=("", 20), bg="white")
        bottom_sensor_distance_text.place(relx=0.457, rely=0.5, anchor=N)

        close_connection = Button(window, text="Close Connection", font=("", 20), command=lambda: Main.exit(s))
        close_connection.place(relx=0.85, rely=0.92, anchor=N)

        dance_button = Button(window, text="Dance", font=("", 20), command=lambda: Main.motor(s, "dance"))
        dance_button.place(relx=0.1, rely=0.2, anchor=N)
        autopilot_button = Button(window, text="Autopilot", font=("", 20), command=lambda: Main.autopilot_choice(window, s))
        autopilot_button.place(relx=0.1, rely=0.3, anchor=N)
        follow_object_button = Button(window, text="Follow Object", font=("", 20), command=lambda: Main.follow_object(window, s))
        follow_object_button.place(relx=0.1, rely=0.4, anchor=N)
        security_camera_button = Button(window, text="Security Camera", font=("", 20), command=lambda: Main.security_camera(window, s))
        security_camera_button.place(relx=0.1, rely=0.5, anchor=N)
        website_button = Button(window, text="Website", font=("", 20), command=lambda: Main.website(window, s))
        website_button.place(relx=0.1, rely=0.6, anchor=N)
        camera_button = Button(window, text="Face Recognition", font=("", 20), command=lambda: Main.camera(follow_object_button, security_camera_button, s))
        camera_button.place(relx=0.1, rely=0.7, anchor=N)
        if website == True:
            website_button['state'] = 'normal'
        else:
            website_button['state'] = 'disabled'

        shutdown_button = Button(window, text="SHUTDOWN", font=("", 15), command=lambda: Main.shutdown(window, s))
        shutdown_button.place(rely=0.03, relx=0.92, anchor=N)

        window.mainloop()

def connect(statues, window, connect_button):
    global IP
    global port

    s = socket.socket()

    try:
        print(f"[*] Connecting to {IP} on port {port}")
        s.connect((IP, port))
    except:
        connect_button.config(text="Failed", bg="red")
        statues.config(text="Disconnected")
        window.after(3000, lambda:Main.connection_error(window, statues, connect_button))

    connect_button.config(bg="lime", fg="white", text="Connecting")
    statues.config(text=f"Connected To: {IP}")

    try:
        s.send("connected".encode())
    except:
        statues.config(text="Disconnected")
        window.after(3000, lambda:Main.connection_error(window, statues, connect_button))

    window.after(3000, lambda:print(""))
    statues.config(text=f"Loading Connection With {IP}")
    window.after(6000, lambda:Main.window(window, s))
    
def connection_window():
    window = Tk()
    window.geometry("600x400")
    window.configure(bg="white")
    window.title("client connection")
    window.resizable(False, False)

    title = Label(window, text="Raspberry Pi Client", font=("", 25), bg="white")
    title.place(relx=0.26, anchor=N)
    credits = Label(window, text="Coded By Karim", font=("", 15), bg="white")
    credits.place(relx=0.15, rely=0.1, anchor=N)

    statues = Label(window, text=f"Disconnected", font=("", 15), bg="white")
    statues.place(rely=0.5, relx=0.5, anchor=N)
    print("[-] Connection statues: disconnected")

    connect_button = Button(window, text="Connect", font=("", 15), bg="red", command=lambda: connect(statues, window, connect_button))
    connect_button.place(rely=0.88, relx=0.9, anchor=N)

    window.mainloop()


if __name__ == "__main__":
    connection_window()
