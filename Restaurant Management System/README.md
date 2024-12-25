# Restaurant Management System

## Project Overview
The Restaurant Management System is a GUI-based desktop application designed to help restaurant owners manage orders and billing efficiently. This application provides an intuitive interface for adding food and drink items, calculating costs, generating bills, and saving or sending bills via SMS. 

## Features
- **Menu Management**: Select food and drink items with quantity inputs.
- **Billing System**: Automatically calculate total cost, including taxes and service charges.
- **Bill Receipt**: Generate a detailed bill with item-wise cost breakdown.
- **Save Bills**: Save bills as text files for record-keeping.
- **Send Bills via SMS**: Send bills directly to customers through SMS (API key required).
- **Calculator Integration**: Perform basic arithmetic calculations for quick price adjustments.

## Prerequisites
- **Python Version**: Python 3.x
- **Required Libraries**: 
  - `tkinter` for GUI components.
  - `requests` for SMS integration.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd restaurant-management-system
   ```
3. Install dependencies:
   ```bash
   pip install requests
   ```
4. Run the application:
   ```
   python resturent.py
   ```

## Usage
1. Launch the application.
2. Select the desired food and drink items, and input quantities.
3. Click **Total** to calculate costs.
4. Use **Save** to save the bill locally.
5. Click **Send** to send the bill via SMS (API key setup required).
6. Use the integrated calculator for additional calculations.
7. Exit the application using the **Exit** button.

## Configuration
- **SMS API Key Setup**: 
  1. Sign up at [Fast2SMS](https://www.fast2sms.com/) or any SMS provider.
  2. Replace the `api` variable inside the `send_bill()` function with your API key.

## File Structure
```
.
├── resturent.py          # Main Python script
├── README.md            # Project documentation
```

## Limitations
- SMS feature requires an active internet connection.
- API key for SMS service needs manual configuration.

## Future Improvements
- Database integration for order history.
- User authentication and role management.
- Enhanced UI design and responsiveness.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Author
Developed by [Vaibhav Rakshe].

