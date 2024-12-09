import turtle

# Initialize game variables
cookies = 0
total_cookies_earned = 0
cookies_per_click = 1
cookies_per_second = 0

# Upgrade settings
upgrades = {
    "cursor": {"cost": 10, "cps": 1, "amount": 0},
    "grandma": {"cost": 50, "cps": 5, "amount": 0},
    "farm": {"cost": 200, "cps": 15, "amount": 0},
    "mine": {"cost": 1000, "cps": 50, "amount": 0},
    "factory": {"cost": 5000, "cps": 200, "amount": 0},
    "bank": {"cost": 20000, "cps": 500, "amount": 0},
}

# Set up the screen
screen = turtle.Screen()
screen.title("Cookie Clicker")
screen.setup(width=800, height=800)
screen.bgcolor("lightyellow")

# Create the clickable cookie
cookie = turtle.Turtle()
cookie.shape("circle")
cookie.color("saddlebrown")
cookie.shapesize(stretch_wid=7, stretch_len=7)
cookie.penup()
cookie.goto(0, 100)

# Display elements
stats_display = {
    "cookies": {"y_pos": 300, "font": ("Arial", 24, "bold"), "content": ""},
    "cps": {"y_pos": 260, "font": ("Arial", 18, "bold"), "content": ""},
    "total": {"y_pos": 220, "font": ("Arial", 18, "bold"), "content": ""},
}
displays = {}

for stat, config in stats_display.items():
    display = turtle.Turtle()
    display.hideturtle()
    display.penup()
    display.goto(0, config["y_pos"])
    displays[stat] = display

# Upgrade buttons and labels
buttons = {}
button_labels = {}
upgrade_positions = {
    "cursor": (-175, -100), "grandma": (0, -100), "farm": (175, -100),
    "mine": (-175, -250), "factory": (0, -250), "bank": (175, -250)
}

for upgrade, position in upgrade_positions.items():
    # Create button
    btn = turtle.Turtle()
    btn.shape("square")
    btn.color("lightblue")
    btn.shapesize(stretch_wid=3, stretch_len=8)
    btn.penup()
    btn.goto(position)
    buttons[upgrade] = btn

    # Add label below button
    label = turtle.Turtle()
    label.hideturtle()
    label.penup()
    label.goto(position[0], position[1] - 20)
    button_labels[upgrade] = label

# Function to update displays
def update_display():
    global stats_display
    # Update main stats only if changed
    for stat, config in stats_display.items():
        current_value = ""
        if stat == "cookies":
            current_value = f"Cookies: {cookies}"
        elif stat == "cps":
            current_value = f"CPS: {cookies_per_second}"
        elif stat == "total":
            current_value = f"Total Cookies Earned: {total_cookies_earned}"

        if config["content"] != current_value:  # Update only if there's a change
            config["content"] = current_value
            displays[stat].clear()
            displays[stat].write(current_value, align="center", font=config["font"])

    # Update button labels
    for upgrade, label in button_labels.items():
        upgrade_info = upgrades[upgrade]
        label_content = (
            f"{upgrade.capitalize()}\nCost: {upgrade_info['cost']}\nCPS: +{upgrade_info['cps']}\n"
            f"Purchased: {upgrade_info['amount']} times"
        )
        label.clear()
        label.write(label_content, align="center", font=("Arial", 10, "bold"))

# Function to handle cookie clicks
def click_cookie(x, y):
    global cookies, total_cookies_earned
    cookies += cookies_per_click
    total_cookies_earned += cookies_per_click
    update_display()

# Function to purchase upgrades
def buy_upgrade(upgrade_name):
    global cookies, cookies_per_second
    upgrade = upgrades[upgrade_name]
    if cookies >= upgrade["cost"]:
        cookies -= upgrade["cost"]
        upgrade["amount"] += 1
        cookies_per_second += upgrade["cps"]
        upgrade["cost"] = int(upgrade["cost"] * 1.25)  # Scale cost
        update_display()
    else:
        print(f"Not enough cookies to buy {upgrade_name.capitalize()}.")

# Event handlers for upgrade buttons
def create_button_handler(upgrade_name):
    def handler(x, y):
        buy_upgrade(upgrade_name)
    return handler

for upgrade, btn in buttons.items():
    btn.onclick(create_button_handler(upgrade))

# Attach click event to cookie
cookie.onclick(click_cookie)

# Game loop for automatic cookie generation
def update_cookies():
    global cookies, total_cookies_earned
    cookies += cookies_per_second
    total_cookies_earned += cookies_per_second
    update_display()
    screen.ontimer(update_cookies, 100)

# Start game loop
update_cookies()
turtle.done()
