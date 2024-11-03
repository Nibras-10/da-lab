def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            row = line.strip().split(',')
            features = row[1:-1]  # Age, income, student, credit_rating
            label = row[-1]       # buys_computer
            data.append((features, label))
    return data

# Step 2: Calculate Prior Probabilities P(class)
def calculate_prior_probabilities(data):
    total_samples = len(data)
    class_counts = {}

    for features, label in data:
        if label not in class_counts:
            class_counts[label] = 0
        class_counts[label] += 1

    priors = {}
    for label in class_counts:
        priors[label] = class_counts[label] / total_samples

    return priors

# Step 3: Calculate Likelihood P(feature|class)
def calculate_likelihoods(data):
    feature_counts = {}
    class_counts = {}

    for features, label in data:
        if label not in class_counts:
            class_counts[label] = 0
            feature_counts[label] = [{} for _ in range(len(features))]
        
        class_counts[label] += 1

        for i in range(len(features)):
            feature_value = features[i]
            if feature_value not in feature_counts[label][i]:
                feature_counts[label][i][feature_value] = 0
            feature_counts[label][i][feature_value] += 1

    likelihoods = {}

    for label in feature_counts:
        likelihoods[label] = []
        
        for i in range(len(feature_counts[label])):
            feature_likelihoods = {}
            
            for feature_value in feature_counts[label][i]:
                feature_likelihoods[feature_value] = feature_counts[label][i][feature_value] / class_counts[label]
            
            likelihoods[label].append(feature_likelihoods)

    return likelihoods

# Step 4: Classify new data and print probabilities
def classify(priors, likelihoods, new_data):
    posteriors = {}
    for label in priors:
        posteriors[label] = priors[label]
        for i in range(len(new_data)):
            if new_data[i] in likelihoods[label][i]:
                posteriors[label] *= likelihoods[label][i][new_data[i]]
            else:
                posteriors[label] *= 0

    # Print the posterior probabilities for each class
    for label in posteriors:
        print(f"Posterior probability for {label}: {posteriors[label]}")

    return max(posteriors, key=posteriors.get)

# Step 5: Running the classifier on new data
def naive_bayes_classifier(training_data, new_data):
    priors = calculate_prior_probabilities(training_data)
    likelihoods = calculate_likelihoods(training_data)
    return classify(priors, likelihoods, new_data)

# Main execution
filename = 'bayes.csv'  # Name of your CSV file
training_data = read_csv_file(filename)

# Classify the new data: X = (age=youth, income=medium, student=yes, credit_rating=fair)
new_sample = ['youth', 'medium', 'yes', 'fair']
predicted_class = naive_bayes_classifier(training_data, new_sample)
print(f'Predicted class for {new_sample}: {predicted_class}')
