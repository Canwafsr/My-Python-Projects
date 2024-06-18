import random 

# Generate a random number between 1 and 100
number = int(random.uniform(1,100))

# Number of guesses allowed for the user
guess = 7

# Counter for the number of attempts
tour = 0

# Game loop
while True:
    choice = int(input("Guess a number from 1 to 100:"))

    if guess != 1:
        if choice > number:
            guess -= 1
            print(f"You guessed a large number, try again.\nRemaining right to guess: {guess}")
            tour += 1
        elif choice < number:
            guess -= 1
            print(f"You guessed a small number, try again.\nRemaining right to guess: {guess}")

        elif choice == number:
            print("Your guess is correct, congratulations\n",
                  f"Our secret number: {number}\n", 
                  f"You tried {tour} times and got the right result")
            tour += 1
            break
    else:
        print(f"You've run out of guesses.\nOur secret number was {number}")
        break

