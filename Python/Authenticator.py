import requests
from flask import jsonify, render_template, request


# Define the external authentication URL
auth_url = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'


# Define the authenticate function to handle /authenticate
def authenticate(email, password):
    try:

        # Get the user credentials
        credentials = {
            "email": email,
            "password": password
        }

        # Validate that the required fields are present
        if not credentials or not all(k in credentials for k in ("email", "password")):
            return jsonify({"message": "Email and password are required"}), 400

        # Send the credentials to the external authentication API
        response = requests.post(auth_url, json=credentials)

        # Handle the response from the external API
        if response.status_code == 200:
            try:
                # Parse the JSON response
                response_data = response.json()

                if response_data[1] == "True":
                    # Return success if authentication was successful
                    return "True"
                else:
                    # Return failure if failed
                    return "False"

            except requests.JSONDecodeError:
                # Handle invalid JSON responses
                return jsonify({"message": "Invalid response from authentication server"}), 500

        # Handle authentication failure
        elif response.status_code == 401:
            return jsonify({"message": "Authentication failed"}), 401

        # Handle other error codes
        else:
            return jsonify({"message": "Unexpected error from authentication server"}), response.status_code

    except Exception as e:
        # Handle unexpected exceptions
        return jsonify({"error": str(e)}), 500
