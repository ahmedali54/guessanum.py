import random
import sqlite3

def create_table():
    con = sqlite3.connect("AhmedAli\guess_game.db")
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_results (
        id INTEGER PRIMARY KEY,
        player_name TEXT,
        secret_number INTEGER,
        attempts INTEGER)''')

    con.commit()
    con.close()

def guess_the_number():
    create_table()
    
    player_name = input("Welcome to Guess the Number!\nWhat's your name? ")
    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0

    print(f"Hello, {player_name}! I'm thinking of a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Take a guess: "))
            attempts += 1

            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(f"Congratulations, {player_name}! You guessed the number in {attempts} attempts!")
                
                # Store the game result in the database
                con = sqlite3.connect("AhmedAli\guess_game.db")
                cursor = con.cursor()
                cursor.execute("INSERT INTO game_results (player_name, secret_number, attempts) VALUES (?, ?, ?)",
                    (player_name, secret_number, attempts))
                con.commit()
                con.close()
                break

        except ValueError:
            print("Please enter a valid number.")

def check_game_results():
    con = sqlite3.connect("AhmedAli\guess_game.db")
    cursor = con.cursor()
    cursor.execute("SELECT player_name, secret_number, attempts FROM game_results")
    results = cursor.fetchall()
    con.close()

    print("\nGame Results:")
    for result in results:
        player_name, secret_number, attempts = result
        print(f"Player: {player_name}, Secret Number: {secret_number}, Attempts: {attempts}")

def further_options():
        option = input("Options:\n1. Delete a record by record ID\n2. Delete all records\n")
        if option == '1':
            # Delete a specific record by ID
            delete_option = input("Enter record ID to delete: ")
            try:
                record_id_to_delete = int(delete_option)
                con = sqlite3.connect("AhmedAli\guess_game.db")
                cursor = con.cursor()
                cursor.execute("DELETE FROM game_results WHERE id = ?", (record_id_to_delete,))
                con.commit()
                con.close()
                print(f"Record ID {record_id_to_delete} has been deleted.")
            except ValueError:
                print("Invalid input. Please enter a valid record ID.")
        elif option == '2':
            # Delete all records
            con = sqlite3.connect("AhmedAli\guess_game.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM game_results")
            con.commit()
            con.close()
            print("All records have been deleted.")
        else:
            print("Invalid option. Please enter a valid option (1 or 2).")


if __name__ == "__main__":
    guess_the_number()
    check_game_results()
    further_options()