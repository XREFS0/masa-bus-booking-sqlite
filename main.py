"""
Developed by MASA
All Rights Reserved.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class BusBookingManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("MASA - Bus Booking & Transit Dispatch System")
        self.root.geometry("1100x660")
        self.root.configure(bg="#0f172a")

        self.init_db()
        self.setup_ui()
        self.fetch_bookings()

    def init_db(self):
        self.conn = sqlite3.connect("bus_dispatch.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                ticket_id TEXT PRIMARY KEY,
                passenger_name TEXT NOT NULL,
                route TEXT NOT NULL,
                bus_type TEXT NOT NULL,
                seat_no TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                fare REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)
        self.cur.execute("SELECT COUNT(*) FROM bookings")
        if self.cur.fetchone()[0] == 0:
            sample = [
                ("TCK-3301", "Marcus Aurelius", "Metropolis -> Capital Central", "Luxury Sleeper AC", "Seat 04", "08:30 AM", 45.00, "Confirmed"),
                ("TCK-3302", "Elena Rostova", "North Coast -> Bay Harbor", "Executive Express", "Seat 12", "10:15 AM", 32.50, "Confirmed"),
                ("TCK-3303", "James Holden", "Oasis Springs -> Metro City", "Standard Cruiser", "Seat 19", "01:00 PM", 25.00, "Checked In"),
                ("TCK-3304", "Naomi Nagata", "Highland Ridge -> Downtown", "Luxury Sleeper AC", "Seat 08", "04:45 PM", 48.00, "Confirmed"),
                ("TCK-3305", "Amos Burton", "South Terminal -> West Hub", "Executive Express", "Seat 21", "07:30 PM", 35.00, "Boarding"),
            ]
            self.cur.executemany("INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?)", sample)
            self.conn.commit()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e293b", foreground="#f8fafc", fieldbackground="#1e293b", rowheight=28, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#334155", foreground="#38bdf8", font=("Segoe UI", 10, "bold"))

        hdr = tk.Frame(self.root, bg="#0369a1", height=65)
        hdr.pack(fill="x")
        tk.Label(hdr, text="MASA Bus Booking & Fleet Dispatch Management", font=("Segoe UI", 19, "bold"), fg="#ffffff", bg="#0369a1").pack(side="left", padx=25, pady=15)
        tk.Label(hdr, text="Architect: MASA | Licensed to: XREFS0", font=("Segoe UI", 10), fg="#bae6fd", bg="#0369a1").pack(side="right", padx=25, pady=20)

        body = tk.Frame(self.root, bg="#0f172a")
        body.pack(fill="both", expand=True, padx=20, pady=15)

        sidebar = tk.Frame(body, bg="#1e293b", width=220)
        sidebar.pack(side="left", fill="y", padx=(0, 15))

        for btn_t in ["Passenger Manifest", "Book Ticket", "Seat Matrix Map", "Bus Fleet Schedule", "Cancel & Refund", "Route Analytics"]:
            tk.Button(sidebar, text=btn_t, font=("Segoe UI", 10, "bold"), fg="#f8fafc", bg="#334155", relief="flat", pady=9, cursor="hand2").pack(fill="x", padx=10, pady=5)

        content = tk.Frame(body, bg="#1e293b")
        content.pack(side="right", fill="both", expand=True)

        stats = tk.Frame(content, bg="#1e293b")
        stats.pack(fill="x", padx=15, pady=15)

        for t, v, c in [("Scheduled Buses", "24", "#38bdf8"), ("Booked Seats", "612", "#4ade80"), ("Load Factor", "89.4%", "#facc15"), ("Today Revenue", "$19,580.00", "#f43f5e")]:
            f = tk.Frame(stats, bg="#334155", padx=14, pady=9)
            f.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(f, text=t, font=("Segoe UI", 9), fg="#94a3b8", bg="#334155").pack(anchor="w")
            tk.Label(f, text=v, font=("Segoe UI", 15, "bold"), fg=c, bg="#334155").pack(anchor="w")

        cols = ("Ticket ID", "Passenger Name", "Route Corridor", "Bus Service", "Seat", "Departure", "Fare", "Status")
        self.tree = ttk.Treeview(content, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110, anchor="center")
        self.tree.column("Passenger Name", width=150, anchor="w")
        self.tree.column("Route Corridor", width=190, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def fetch_bookings(self):
        self.cur.execute("SELECT * FROM bookings")
        for row in self.cur.fetchall():
            formatted = list(row)
            formatted[6] = f"${formatted[6]:.2f}"
            self.tree.insert("", "end", values=formatted)

if __name__ == "__main__":
    root = tk.Tk()
    app = BusBookingManagementSystem(root)
    root.mainloop()
