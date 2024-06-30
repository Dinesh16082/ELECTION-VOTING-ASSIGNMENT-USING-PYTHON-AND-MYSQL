import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="election_db"
)
cursor = db_connection.cursor()
def conduct_voting():
    cursor.execute("SELECT candidate_id, name, party FROM candidates")
    candidates = cursor.fetchall()
    print("Candidates:")
    for candidate in candidates:
        print(f"{candidate[0]}. {candidate[1]} - {candidate[2]}")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    candidate = int(input("Enter candidate ID to vote: "))

    # Update the voters table to mark the voter as voted
    cursor.execute("UPDATE voters SET voted = TRUE WHERE email = %s", (email,))
    db_connection.commit()

    # Insert voter details into the voters table
    insert_query = "INSERT INTO voters (name, email, voted) VALUES (%s, %s, %s)"
    voter_data = (name, email, True)
    cursor.execute(insert_query, voter_data)
    db_connection.commit()

    send_email(email, name)
    print("Thank you for voting!")

def send_email(email, name):
    from_email = "dineshdinesh112004@gmail.com"
    password = "zrdp fmqe dawq bxkg"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = "Thank You for Voting!"
    body = f"Dear {name},\n\nThank you for participating in the election.\n\nBest regards,\nThe Election Team"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, password)
    text = msg.as_string()
    server.sendmail(from_email, email, text)
    server.quit()
if __name__ == "__main__":
    conduct_voting()
cursor.close()
db_connection.close()
