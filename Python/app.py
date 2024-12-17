from flask import jsonify, render_template, request
import connexion
import pyodbc


# Initialize the Flask app and add the API
app = connexion.App(__name__, specification_dir="./")

# Define the database connection
DATABASE_CONFIG = {
    "server": "DIST-6-505.uopnet.plymouth.ac.uk" ,
    "database": "COMP2001_JCavanagh",
    "username": "JCavanagh",
    "password": "CbiN632+"
}


# Establish a connection to my database
def get_db_connection():
    conn_string = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DATABASE_CONFIG['server']};"
        f"DATABASE={DATABASE_CONFIG['database']};"
        f"UID={DATABASE_CONFIG['username']};"
        f"PWD={DATABASE_CONFIG['password']}"
    )
    return pyodbc.connect(conn_string)

def get_trails():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
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
        conn.close()
        return jsonify(trails)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

def create_trail():
    
    try:

        # Parse JSON data from the request body
        trail_data = request.get_json()

        # Extract individual fields
        trail_name = trail_data.get("trail_name")
        trail_summary = trail_data.get("trail_summary")
        trail_description = trail_data.get("trail_description")
        difficulty = trail_data.get("difficulty")
        location = trail_data.get("location")
        trail_length = trail_data.get("trail_length")
        trail_elevation = trail_data.get("trail_elevation")
        route_type = trail_data.get("route_type")
        trail_feature = trail_data.get("trail_feature")

        # Input validation (ensure required fields are present)
        if not all([trail_name, trail_summary, trail_description, difficulty, location, trail_length, trail_elevation, route_type, trail_feature]):
            return jsonify({"error": "Missing required trail fields"}), 400

        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Call the stored procedure to insert a new trail
        cursor.execute(
            "EXEC CW2.insertintotrail ?, ?, ?, ?, ?, ?, ?, ?, ?",
            (
                trail_name,
                trail_summary,
                trail_description,
                difficulty,
                location,
                trail_length,
                trail_elevation,
                route_type,
                trail_feature
            )
        )

        # Commit the transaction
        conn.commit()   
        # Close the connection
        cursor.close()
        conn.close()    
        # Return a success response
        return jsonify({"message": "Trail created successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.add_api("swagger.yml")


@app.route("/")

def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)