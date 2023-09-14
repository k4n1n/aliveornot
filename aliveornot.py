import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
from threading import Thread
from time import sleep
import pickle
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain Status Checker")

        self.data_file = 'hosts_data.pkl'

        if os.path.exists(self.data_file):
            with open(self.data_file, 'rb') as f:
                self.domains = pickle.load(f)
        else:
            self.domains = {}

        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=1)

        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill=tk.X, pady=5)

        self.add_button = tk.Button(self.buttons_frame, text="Add Host", command=self.add_host)
        self.add_button.pack(side=tk.LEFT, padx=10)

        self.remove_button = tk.Button(self.buttons_frame, text="Remove Host", command=self.remove_host)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        self.ping_button = tk.Button(self.buttons_frame, text="Ping Now", command=self.ping_now, width=15)
        self.ping_button.pack(side=tk.LEFT, padx=10)

        for host, data in self.domains.items():
            ip_address = self.get_ip_address(host)
            status_color = data['status']
            self.listbox.insert(tk.END, f"■ {host} ({ip_address})")
            self.listbox.itemconfig(tk.END, foreground=status_color)

        self.update_thread = Thread(target=self.update_status)
        self.update_thread.daemon = True
        self.update_thread.start()

    def add_host(self):
        host = simpledialog.askstring("Add Host", "Enter the domain/host:")
        if host:
            if host not in self.domains:
                self.domains[host] = {'status': 'gray'}
                ip_address = self.get_ip_address(host)
                self.listbox.insert(tk.END, f"■ {host} ({ip_address})")
                self.listbox.itemconfig(tk.END, foreground="gray")
                self.save_data()
            else:
                messagebox.showerror("Error", "Host already added.")

    def remove_host(self):
        selected = self.listbox.curselection()
        if selected:
            host = self.listbox.get(selected[0]).split("■ ")[1].split(" ")[0]
            if host in self.domains:
                del self.domains[host]
                self.listbox.delete(selected[0])
                self.save_data()

    def get_ip_address(self, host):
        try:
            ip_address = socket.gethostbyname(host)
            return ip_address
        except:
            return "Unresolved"

    def is_host_alive(self, host):
        if host == "localhost":
            return True
        try:
            socket.create_connection((host, 80), 2)
            return True
        except:
            return False

    def update_status(self):
        while True:
            self.ping_all_hosts()
            sleep(120)  # check every 2 minutes

    def ping_now(self):
        self.ping_all_hosts()

    def ping_all_hosts(self):
        for idx, item in enumerate(self.listbox.get(0, tk.END)):
            host = item.split("■ ")[1].split(" ")[0]
            status = "black" if self.get_ip_address(host) == "Unresolved" else ("green" if self.is_host_alive(host) else "red")
            self.domains[host]['status'] = status
            self.listbox.itemconfig(idx, foreground=status)

    def save_data(self):
        with open(self.data_file, 'wb') as f:
            pickle.dump(self.domains, f)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Set initial size
    app = App(root)
    root.mainloop()
