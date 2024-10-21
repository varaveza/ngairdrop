import requests
import time
import random
import json

# Fixed init_data
INIT_DATA = "query_id=AAFb_CxpAAAAAFv8LGlYhy55&user=%7B%22id%22%3A1764555867%2C%22first_name%22%3A%22Ardan%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22Herodutro%22%2C%22language_code%22%3A%22en%22%2C%22allows_write_to_pm%22%3Atrue%7D&auth_date=1729435075&hash=67a87a980061e02984fd0349ba35fa5477b202f34805b00e3ce6d65b6e96b042"

def login():
    url = "https://api-web.tomarket.ai/tomarket-game/v1/user/login"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://mini-app.tomarket.ai",
        "referer": "https://mini-app.tomarket.ai/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    payload = {
        "init_data": INIT_DATA,
        "invite_code": "",
        "from": "",
        "is_bot": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data.get("data", {}).get("access_token")
        if access_token:
            print("Login successful. Access token obtained.")
            return access_token
    print("Login failed.")
    return None

def get_balance(access_token, print_balance=True):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/user/balance"
    headers = {
        "accept": "application/json, text/plain, */*",
        "authorization": access_token,
        "origin": "https://mini-app.tomarket.ai",
        "referer": "https://mini-app.tomarket.ai/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        play_passes = response_data.get("data", {}).get("play_passes", 0)
        available_balance = response_data.get("data", {}).get("available_balance", 0)
        if print_balance:
            print(f"Current balance: {play_passes} ticket")
            print(f"Available balance: {available_balance}")
        return play_passes, available_balance
    print("Failed to get balance.")
    return 0, 0

def play_game(game_id, auth_token, headers):
    url = "https://api-web.tomarket.ai/tomarket-game/v1/game/play"
    payload = {
        "game_id": game_id
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("data"):
            round_id = response_data["data"].get("round_id")
            if round_id:
                print("Game Playing Wait 30 Seconds! Round ID:", round_id)
                return round_id
    return None

def claim_reward(game_id, auth_token, headers):
    points = random.randint(450, 600)
    url = "https://api-web.tomarket.ai/tomarket-game/v1/game/claim"
    payload = {
        "game_id": game_id,
        "points": points
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("data"):
            points_claim = response_data["data"].get("points")
            if points_claim:
                print("Success Claim", points_claim, "points")
                return points_claim

# Main script
access_token = login()

if not access_token:
    print("Failed to obtain access token. Exiting.")
    exit()

game_id = "59bcd12e-04e2-404c-a172-311a0084587d"

headers = {
    "accept": "application/json, text/plain, */*",
    "authorization": access_token,
    "content-type": "application/json",
    "origin": "https://mini-app.tomarket.ai",
    "referer": "https://mini-app.tomarket.ai/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
}

# Display initial balance
initial_play_passes, initial_balance = get_balance(access_token)
print(f"Initial available balance: {initial_balance}")

while True:
    play_passes, _ = get_balance(access_token, print_balance=False)
    if play_passes <= 0:
        print("No more ticket left. Exiting.")
        # Display final balance
        _, final_balance = get_balance(access_token)
        print(f"Final available balance: {final_balance}")
        break

    round_id = play_game(game_id, access_token, headers)
    if round_id:
        time.sleep(30)
        claim_reward(game_id, access_token, headers)
        delay = random.randint(5, 15)
        print(f"Waiting for {delay} seconds before the next play")
        time.sleep(delay)
    else:
        print("Failed to start game. Exiting.")
        # Display final balance
        _, final_balance = get_balance(access_token)
        print(f"Final available balance: {final_balance}")
        break
