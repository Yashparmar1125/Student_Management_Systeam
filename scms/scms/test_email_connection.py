import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('studentmanagementsystem71@gmail.com', 'Yash@123')  # Replace with your email and password
    print("Login successful!")
    server.quit()
except Exception as e:
    print("Error:", e)

    # FdkQW@87Ujk12345678
    #1A7GW5MHW1K6DRRAP7FCU7PR
    #e96da50360017f345a0990cecf198b8d-784975b6-6365575c api key mailgun
