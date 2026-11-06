while True:

    print("\n========== AQIEXPLAINER MENU ==========")

    print("1. About AQIExplainer")
    print("2. Sample Questions")
    print("3. Check AQI Category")
    print("0. Exit")

    print("=======================================")

    choice = input("\nEnter your choice: ")

    if choice == "1":

        print("\nAQIExplainer is an Air Quality Information System.")
        print("It helps users understand air pollution")
        print("levels across Maharashtra cities.")

    elif choice == "2":

        print("\nSample Questions:")

        print("1. What is the AQI of Nagpur?")
        print("2. Which city has poor air quality?")
        print("3. What is PM2.5?")
        print("4. What does Severe AQI mean?")

    elif choice == "3":

        try:
            aqi = int(input("\nEnter AQI value (0-500): "))

            if aqi < 0 or aqi > 500:
                print("Invalid AQI value.")

            elif aqi <= 50:
                print("AQI Category: Good")

            elif aqi <= 100:
                print("AQI Category: Satisfactory")

            elif aqi <= 200:
                print("AQI Category: Moderate")

            elif aqi <= 300:
                print("AQI Category: Poor")

            elif aqi <= 400:
                print("AQI Category: Very Poor")

            else:
                print("AQI Category: Severe")

        except ValueError:
            print("Please enter a valid whole number.")

    elif choice == "0":

        print("\nThank you for using AQIExplainer!")

        break

    else:

        print("\nInvalid choice. Please select again.")
