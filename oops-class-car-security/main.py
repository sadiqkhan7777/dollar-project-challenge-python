import streamlit as st 
import secrets
import datetime

# ==============================
# OOP Classes
# ==============================

class User:
    def __init__(self, name, gender, email, phone, national_id):
        self.name = name
        self.gender = gender
        self.email = email
        self.phone = phone
        self.national_id = national_id
        self.registered_cars = []

    def register_car(self, car):
        self.registered_cars.append(car)


class Car:
    def __init__(self, plate_number, model, car_type, owner: User):
        self.plate_number = plate_number
        self.model = model
        self.car_type = car_type
        self.owner = owner
        self.is_locked = True
        self.tracking_enabled = True
        self.bonnet_secure = True
        self.fuel_tank_secure = True
        self.last_known_location = "Home Area"
        self.is_engine_on = False
        self.last_access_user = None
        self.security_pin = self.generate_pin()
        self.failed_attempts = 0
        self.engine_logs = []
        self.auto_lock = False
        self.safe_location = "Home Area"
        self.face_verified = False
        self.fuel_level = 100  # in percentage

    def generate_pin(self):
        return secrets.randbelow(9000) + 1000

    def regenerate_pin(self):
        self.security_pin = self.generate_pin()

    def simulate_fuel_tampering(self):
        self.fuel_level -= 50
        if self.fuel_level < 50:
            return "⚠️ Alert: Fuel tank tampered!"
        return "✅ Fuel tank secure."

    def simulate_bonnet_open(self):
        self.bonnet_secure = False
        return "🚨 Bonnet opened without authorization!"

    def start_engine(self, user, entered_pin, current_location, face_verified):
        if user != self.owner:
            return AlertSystem.alert_theft(self, "Unauthorized user trying to access the car.")

        if not face_verified:
            return "🔒 Face not verified. Cannot start engine."

        if current_location != self.safe_location:
            return "📍 Car outside of safe zone. Engine locked."

        if entered_pin == self.security_pin:
            self.failed_attempts = 0
            self.is_engine_on = True
            self.is_locked = False
            self.last_access_user = user
            self.engine_logs.append((datetime.datetime.now(), user.name))
            return f"✅ Engine started successfully at {datetime.datetime.now().strftime('%H:%M:%S')}."
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.lock_car()
                return AlertSystem.alert_theft(self, "3 wrong PIN attempts. System locked.")
            return "❌ Incorrect PIN. Try again."

    def lock_car(self):
        self.is_locked = True
        self.is_engine_on = False
        self.auto_lock = True


class AlertSystem:
    @staticmethod
    def alert_theft(car, message):
        return f"🚨 ALERT: {message} Notifying police and owner ({car.owner.name})!"


# ==============================
# Streamlit UI
# ==============================

st.set_page_config(page_title="Secure Car System Pro", layout="centered")
st.title("🚗 Secure Car Tracking & Anti-Theft System (Advanced)")

if "users" not in st.session_state:
    st.session_state.users = []

if "cars" not in st.session_state:
    st.session_state.cars = []

# User Registration
st.subheader("1️⃣ Register User")
with st.form("register_user_form"):
    name = st.text_input("Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    national_id = st.text_input("National ID")
    submitted = st.form_submit_button("Register User")
    if submitted:
        user = User(name, gender, email, phone, national_id)
        st.session_state.users.append(user)
        st.success(f"✅ User {name} registered successfully!")

# Car Registration
st.subheader("2️⃣ Register Car")
if st.session_state.users:
    selected_user = st.selectbox("Select Owner", st.session_state.users, format_func=lambda x: x.name)
    with st.form("register_car_form"):
        plate = st.text_input("Car Plate Number")
        model = st.text_input("Car Model")
        car_type = st.selectbox("Car Type", ["Sports", "Off-Road", "Luxury", "Exotic"])
        submitted_car = st.form_submit_button("Register Car")
        if submitted_car:
            car = Car(plate, model, car_type, selected_user)
            selected_user.register_car(car)
            st.session_state.cars.append(car)
            st.success(f"🚘 Car {plate} registered to {selected_user.name}. PIN: {car.security_pin}")
            st.info(f"🔑 The PIN for {plate} is: {car.security_pin}")  # Displaying PIN after registration
else:
    st.warning("⚠️ Please register a user first.")

# Car Control Panel
st.subheader("3️⃣ Car Control Panel")
if st.session_state.cars:
    selected_car = st.selectbox("Select Car", st.session_state.cars, format_func=lambda c: f"{c.model} ({c.plate_number})")
    st.caption(f"🔐 Dev Hint: Current PIN is {selected_car.security_pin}")  # For testing
    entered_pin = st.text_input("🔑 Enter PIN", type="password")
    current_location = st.selectbox("📍 Current Car Location", ["Home Area", "Unknown", "Street 45"])
    face_verified = st.checkbox("🧑‍🦰 Face Verified")

    if st.button("🔓 Start Engine"):
        if entered_pin.isdigit() and len(entered_pin) == 4:
            pin_int = int(entered_pin)
            response = selected_car.start_engine(selected_car.owner, pin_int, current_location, face_verified)
            st.write(response)
        else:
            st.error("❌ Please enter a valid 4-digit numeric PIN.")

    if st.button("🔒 Lock Car"):
        selected_car.lock_car()
        st.success("🔒 Car locked manually.")

    if st.button("♻️ Regenerate PIN"):
        selected_car.regenerate_pin()
        st.success(f"New secure PIN: {selected_car.security_pin}")

    if st.button("🚨 Emergency Shutdown"):
        selected_car.lock_car()
        st.error("❌ Emergency shutdown activated. Police notified.")

    if st.button("⛽ Simulate Fuel Tank Tampering"):
        st.warning(selected_car.simulate_fuel_tampering())

    if st.button("🔧 Simulate Bonnet Tampering"):
        st.warning(selected_car.simulate_bonnet_open())

# Registered Users and Cars
st.subheader("4️⃣ Registered Users and Cars")
for user in st.session_state.users:
    with st.expander(f"👤 {user.name} ({user.gender})"):
        st.write(f"📧 Email: {user.email}")
        st.write(f"📱 Phone: {user.phone}")
        st.write(f"🆔 National ID: {user.national_id}")

        if user.registered_cars:
            for car in user.registered_cars:
                st.markdown(f"""
                    - **Model**: {car.model}  
                    - **Plate**: {car.plate_number}  
                    - **Type**: {car.car_type}  
                    - **PIN**: {car.security_pin}  
                    - **Locked**: {"🔒 Yes" if car.is_locked else "🔓 No"}  
                    - **Engine On**: {"🟢 Yes" if car.is_engine_on else "🔴 No"}  
                    - **Fuel Level**: {car.fuel_level}%  
                    - **Bonnet Secure**: {"✅" if car.bonnet_secure else "⚠️ No"}  
                """)
                if car.engine_logs:
                    st.markdown("**⏱️ Engine Start Logs:**")
                    for log in car.engine_logs:
                        st.write(f"🕒 {log[0]} by {log[1]}")
        else:
            st.info("No cars registered.")
