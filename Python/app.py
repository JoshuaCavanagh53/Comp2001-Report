from flask import jsonify, render_template, request
import connexion
import pyodbc
from Authenticator import authenticate


# Initialize the Flask app and add the API
app = connexion.App(__name__, specification_dir="./")

# Define the database connection
DATABASE_CONFIG = {
    "server": "DIST-6-505.uopnet.plymouth.ac.uk",
    "database": "COMP2001_JCavanagh",
    "username": "JCavanagh",
    "password": "CbiN632+"
}


# Establish a connection to the database
def get_db_connection():
    conn_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )
    return pyodbc.connect(conn_string)


# Get all current trails stored in the database
def get_trails():
    conn = None
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the stored procedure
        cursor.execute("EXEC CW2.readtrail")
        rows = cursor.fetchall()

        # Convert rows into a dictionary
        trails = [
            {
                "trail_id": row.trail_id,
                "trail_name": row.trail_name,
                "trail_summary": row.trail_summary,
                "trail_description": row.trail_description,
                "difficulty": row.difficulty,
                "location": row.location,
                "trail_length": row.trail_length,
                "trail_elevation": row.trail_elevation,
                "route_type": row.route_type,
                "trail_feature": row.trail_feature
            }
            for row in rows
        ]

        return jsonify(trails)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch trails: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


# Add a new trail to the database
def create_trail():
    conn = None
    
    trail_data = request.get_json()

    try:

        if authenticate(trail_data.get("email"), trail_data.get("password")) == "True":
            # Parse JSON data from the request body
            trail_data = request.get_json()

            # Input validation
            required_fields = [
                "trail_name", "trail_summary", "trail_description",
                "difficulty", "location", "trail_length", "trail_elevation",
                "route_type", "trail_feature"
            ]
            if not all(trail_data.get(field) for field in required_fields):
                return jsonify({"error": "Missing required trail fields"}), 400

            # Establish database connection
            conn = get_db_connection()
            cursor = conn.cursor()

            # Call the stored procedure to insert a new trail
            cursor.execute(
                "EXEC CW2.insertintotrail ?, ?, ?, ?, ?, ?, ?, ?, ?",
                (
                    trail_data["trail_name"], trail_data["trail_summary"],
                    trail_data["trail_description"], trail_data["difficulty"],
                    trail_data["location"], trail_data["trail_length"],
                    trail_data["trail_elevation"], trail_data["route_type"],
                    trail_data["trail_feature"]
                )
            )

            conn.commit()
            return jsonify({"message": "Trail created successfully"}), 201

        else:
            return jsonify({"message": "Must be authorized to create a trail"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to create trail: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


# View a trail from the database
def get_trail(trail_id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the stored procedure
        cursor.execute("EXEC CW2.readindividualtrail ?", (trail_id,))
        trail_data = cursor.fetchone()

        if not trail_data:
            return jsonify({"message": "Trail not found"}), 404

        trail = {
            "trail_id": trail_data.trail_id,
            "trail_name": trail_data.trail_name,
            "trail_summary": trail_data.trail_summary,
            "trail_description": trail_data.trail_description,
            "difficulty": trail_data.difficulty,
            "location": trail_data.location,
            "trail_length": trail_data.trail_length,
            "trail_elevation": trail_data.trail_elevation,
            "route_type": trail_data.route_type,
            "trail_feature": trail_data.trail_feature
        }

        return jsonify(trail)

    except Exception as e:
        return jsonify({"error": f"Failed to fetch trail: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


# Delete a trail
def delete_trail(trail_id):
    conn = None
    
    details = request.get_json()
    try:
        
        if authenticate(details.get("email"), details.get("password")) == "True":
           conn = get_db_connection()
           cursor = conn.cursor()
   
           # Check if the trail exists
           cursor.execute("EXEC CW2.readindividualtrail ?", (trail_id,))
           if not cursor.fetchone():
               return jsonify({"message": "Trail not found"}), 404
   
           # Execute the delete stored procedure
           cursor.execute("EXEC CW2.deletetrail ?", (trail_id,))
           conn.commit()
           return jsonify({"message": f"Trail with ID {trail_id} deleted successfully"}), 200
        else:
            return jsonify({"message": "Must be authorized to delete a trail"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to delete trail: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


@app.route('/updatetrail/<int:trail_id>', methods=['PUT'])
def update_trail(trail_id):
    conn = None
    
    trail_data = request.get_json()
    
    try:

        if authenticate(trail_data.get("email"), trail_data.get("password")) == "True":
           conn = get_db_connection()
           cursor = conn.cursor()
   
           # Execute the update stored procedure
           cursor.execute(
               "EXEC CW2.updatetrail ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
               (
                   trail_id,
                   trail_data.get("trail_name"),
                   trail_data.get("trail_summary"),
                   trail_data.get("trail_description"),
                   trail_data.get("difficulty"),
                   trail_data.get("location"),
                   trail_data.get("trail_length"),
                   trail_data.get("trail_elevation"),
                   trail_data.get("route_type"),
                   trail_data.get("trail_feature")
               )
           )
   
           conn.commit()
           return jsonify({"message": "Trail updated successfully"}), 200

        else:
            return jsonify({"message": "Must be authorized to create a trail"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to update trail: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()


# Add the Swagger API
app.add_api("swagger.yml")


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
