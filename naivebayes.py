import csv

# Load dataset from a CSV file
def load_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        data = [tuple(row[1:]) for row in reader]  # Skip the RID column
    return data

# Calculate Naive Bayes probabilities
def calculate_probabilities(data, features):
    # Count occurrences for each class (buys_computer)
    buy_computer_yes = sum(1 for row in data if row[4] == 'yes')
    buy_computer_no = sum(1 for row in data if row[4] == 'no')
    total = len(data)

    # Handle cases where buy_computer_yes or buy_computer_no is zero
    if buy_computer_yes == 0 or buy_computer_no == 0:
        return 0, 0

    # Calculate Prior Probabilities
    P_yes = buy_computer_yes / total
    P_no = buy_computer_no / total

    # Calculate Likelihoods (conditional probabilities) for `buys_computer = yes`
    P_age_given_yes = sum(1 for row in data if row[0] == features['age'] and row[4] == 'yes') / buy_computer_yes
    P_income_given_yes = sum(1 for row in data if row[1] == features['income'] and row[4] == 'yes') / buy_computer_yes
    P_student_given_yes = sum(1 for row in data if row[2] == features['student'] and row[4] == 'yes') / buy_computer_yes
    P_credit_rating_given_yes = sum(1 for row in data if row[3] == features['credit_rating'] and row[4] == 'yes') / buy_computer_yes

    # Calculate Likelihoods (conditional probabilities) for `buys_computer = no`
    P_age_given_no = sum(1 for row in data if row[0] == features['age'] and row[4] == 'no') / buy_computer_no
    P_income_given_no = sum(1 for row in data if row[1] == features['income'] and row[4] == 'no') / buy_computer_no
    P_student_given_no = sum(1 for row in data if row[2] == features['student'] and row[4] == 'no') / buy_computer_no
    P_credit_rating_given_no = sum(1 for row in data if row[3] == features['credit_rating'] and row[4] == 'no') / buy_computer_no

    # Calculate posterior probabilities
    P_yes_given_features = P_yes * P_age_given_yes * P_income_given_yes * P_student_given_yes * P_credit_rating_given_yes
    P_no_given_features = P_no * P_age_given_no * P_income_given_no * P_student_given_no * P_credit_rating_given_no

    return P_yes_given_features, P_no_given_features

# Get user input for features
def get_user_input():
    age = input("Enter age (youth/middle_aged/senior): ").strip().lower()
    income = input("Enter income (high/medium/low): ").strip().lower()
    student = input("Are they a student? (yes/no): ").strip().lower()
    credit_rating = input("Enter credit rating (fair/excellent): ").strip().lower()
    return {'age': age, 'income': income, 'student': student, 'credit_rating': credit_rating}

# Main function to run the Naive Bayes prediction
def main():
    filename = 'bayes.csv'  # Assuming data.csv is the file name with the dataset
    data = load_data(filename)
    features = get_user_input()

    P_yes_given_features, P_no_given_features = calculate_probabilities(data, features)

    # Display results
    print(f"P(yes | features) = {P_yes_given_features:.5f}")
    print(f"P(no | features) = {P_no_given_features:.5f}")

    # Make prediction
    if P_yes_given_features > P_no_given_features:
        print("Predicted: Buys computer = yes")
    else:
        print("Predicted: Buys computer = no")

# Run the program
if __name__ == "__main__":
    main()
