# Movie Ticket Booking System

A user-friendly movie ticket booking application that allows users to register, log in, book tickets, and receive WhatsApp notifications for their bookings.

## Features

- **User Registration**: Users can create an account with a username, password, and WhatsApp phone number.
- **User Login**: Secure login using username and password with OTP verification.
- **Movie Selection**: Users can select from a list of currently showing movies.
- **Ticket Booking**: Book tickets for selected movies and receive a confirmation message via WhatsApp.
- **Input Validation**: Ensures usernames and passwords meet specified criteria.

## Technology Stack

- Python
- SQLite
- Tkinter (for GUI)
- Twilio (for sending WhatsApp notifications)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie_ticket_booking_system.git
   ```
2. Install required packages:
   ```bash
   pip install twilio
   ```

## Twilio Configuration

1. Sign up or log in to your [Twilio account](https://www.twilio.com/).
2. Navigate to the **Twilio Console** and create a new project.
3. Obtain your **Account SID** and **Auth Token** from the project dashboard.
4. Purchase a Twilio number that supports WhatsApp.
5. In your code, replace the following placeholders with your Twilio credentials:
   ```python
   account_sid = 'YOUR_ACCOUNT_SID'
   auth_token = 'YOUR_AUTH_TOKEN'
   twilio_number = 'whatsapp:+YOUR_TWILIO_NUMBER'
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Register or log in using your credentials.
3. Follow the on-screen instructions to book tickets.

## Contributing

Feel free to submit issues or pull requests for enhancements and bug fixes.

## License

This project is licensed under the MIT License.
```
