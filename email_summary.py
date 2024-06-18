import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(summary, performance, recipient_email, preview=False):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    # Calculate overall performance for sorting
    overall_performance = {}
    for ticker, perf in performance.items():
        if perf['12mo'] != 'n/a':
            overall_performance[ticker] = float(perf['12mo'].strip('%'))
        elif perf['6mo'] != 'n/a':
            overall_performance[ticker] = float(perf['6mo'].strip('%'))
        elif perf['1mo'] != 'n/a':
            overall_performance[ticker] = float(perf['1mo'].strip('%'))
        elif perf['5d'] != 'n/a':
            overall_performance[ticker] = float(perf['5d'].strip('%'))
        elif perf['1d'] != 'n/a':
            overall_performance[ticker] = float(perf['1d'].strip('%'))
        else:
            overall_performance[ticker] = 0

    sorted_tickers = sorted(overall_performance, key=overall_performance.get, reverse=True)

    # Generate the current date string
    current_date = datetime.now().strftime("%m/%d/%y")

    # Create the email subject with the dynamic date
    email_subject = f"[{current_date}] Investment Summary - Kingston"

    # Create the email content
    email_body = f"""
    <!doctype html>
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
    <head>
        <title>Stock Highlight Summary</title>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;700px&display=swap" rel="stylesheet">
        <style type="text/css">
            body {{
                margin: 0;
                padding: 0;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
                background-color: #252525;
                font-family: 'Poppins', sans-serif;
            }}
            table, td {{
                border-collapse: collapse;
                mso-table-lspace: 0pt;
                mso-table-rspace: 0pt;
            }}
            img {{
                border: 0;
                height: auto;
                line-height: 100%;
                outline: none;
                text-decoration: none;
                -ms-interpolation-mode: bicubic;
            }}
            p {{
                display: block;
                margin: 13px 0;
            }}
            @media only screen and (max-width:480px) {{
                @-ms-viewport {{
                    width: 320px;
                }}
                @viewport {{
                    width: 320px;
                }}
            }}
            @media only screen and (min-width:480px) {{
                .mj-column-per-100 {{
                    width: 100% !important;
                }}
            }}
        </style>
    </head>
    <body style="background-color:#252525;">
        <div style="background-color:#252525;">
            <div style="background:#252525;background-color:#252525;Margin:0px auto;max-width:700px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#252525;background-color:#252525;width:100%;">
                    <tbody>
                        <tr>
                            <td style="border-bottom:#333957 solid 5px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="background:#f5f5f5;background-color:#f5f5f5;Margin:0px auto;max-width:700px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="background:#f5f5f5;background-color:#f5f5f5;width:100%;">
                    <tbody>
                        <tr>
                            <td style="border:#dddddd solid 1px;border-top:0px;direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                                <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" style="vertical-align:bottom;" width="100%">
                                        <tr>
                                            <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border-spacing:0px;">
                                                    <tbody>
                                                        <tr>
                                                            <td style="width:64px;">
                                                                <img height="auto" src="https://i.imgur.com/JnD9rMc.png" style="border:0;display:block;outline:none;text-decoration:none;width:100%;" width="64" />
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="center" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                <div style="font-family:'Poppins', Arial, sans-serif;font-size:24px;font-weight:bold;line-height:22px;text-align:center;color:#525252;">
                                                    Investment Summary
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                <div style="font-family:'Poppins', Arial, sans-serif;font-size:14px;line-height:22px;text-align:left;color:#525252;">
                                                    <p>Hello,</p>
                                                    <p>Here is the generated report of your stocks' performance:</p>
                                                    <p><strong>Buys today:</strong><br>
                                                    {', '.join(summary['magenta']) if summary['magenta'] else 'None'}</p>
                                                    <p><strong>Sells today:</strong><br>
                                                    {', '.join(summary['orange']) if summary['orange'] else 'None'}</p>
                                                </div>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                <table border="0" style="cellspacing:0;color:#000;font-family:'Poppins', Arial, sans-serif;font-size:13px;line-height:22px;table-layout:auto;width:100%;">
                                                    <tr style="border-bottom:1px solid #ecedee;text-align:left;">
                                                        <th style="padding: 0 15px 10px 0;">Stock</th>
                                                        <th style="padding: 0 15px;">1d</th>
                                                        <th style="padding: 0 15px;">5d</th>
                                                        <th style="padding: 0 15px;">1mo</th>
                                                        <th style="padding: 0 15px;">6mo</th>
                                                        <th style="padding: 0 15px;">12mo</th>
                                                        <th style="padding: 0 15px;">Since Buy</th>
                                                    </tr>
    """
    for ticker in sorted_tickers:
        perf = performance[ticker]
        since_buy = perf.get('since_buy', 'n/a')  # Handle missing 'since_buy' key
        email_body += f"""
                                                    <tr>
                                                        <td style="padding: 5px 15px 5px 0; color: {get_color(perf['1d'])}">{ticker}</td>
                                                        <td style="padding: 0 15px; color: {get_color(perf['1d'])}">{perf['1d']}</td>
                                                        <td style="padding: 0 15px; color: {get_color(perf['5d'])}">{perf['5d']}</td>
                                                        <td style="padding: 0 15px; color: {get_color(perf['1mo'])}">{perf['1mo']}</td>
                                                        <td style="padding: 0 15px; color: {get_color(perf['6mo'])}">{perf['6mo']}</td>
                                                        <td style="padding: 0 15px; color: {get_color(perf['12mo'])}">{perf['12mo']}</td>
                                                        <td style="padding: 0 15px; color: {get_color(since_buy)}">{since_buy}</td>
                                                    </tr>
        """
    email_body += """
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td align="left" style="font-size:0px;padding:10px 25px;word-break:break-word;">
                                                <div style="font-family:'Poppins', Arial, sans-serif;font-size:14px;line-height:20px;text-align:left;color:#f5f5f5;">
                                                    Best regards,<br><br> Kingston Financial Services
                                                </div>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div style="Margin:0px auto;max-width:700px;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="width:100%;">
                    <tbody>
                        <tr>
                            <td style="direction:ltr;font-size:0px;padding:20px 0;text-align:center;vertical-align:top;">
                                <div class="mj-column-per-100 outlook-group-fix" style="font-size:13px;text-align:left;direction:ltr;display:inline-block;vertical-align:bottom;width:100%;">
                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                        <tbody>
                                            <tr>
                                                <td style="vertical-align:bottom;padding:0;">
                                                    <table border="0" cellpadding="0" cellspacing="0" role="presentation" width="100%">
                                                        <tr>
                                                            <td align="center" style="font-size:0px;padding:0;word-break:break-word;">
                                                                <div style="font-family:'Poppins', Arial, sans-serif;font-size:12px;font-weight:300;line-height:1;text-align:center;color:#575757;">
                                                                    Sent from Kingston Financial Services. This email was sent on command.
                                                                </div>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """

    if preview:
        # Save the email body to an HTML file for preview
        with open("email_preview.html", "w") as file:
            file.write(email_body)
        logging.info("Email preview saved to email_preview.html")
        return

    # Set up the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = email_subject
    message.attach(MIMEText(email_body, 'html'))

    # Send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.close()
        logging.info(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")

def get_color(percentage):
    if percentage == 'n/a':
        return 'rgb(245,245,245)'
    percentage = float(percentage.strip('%'))
    if -1 <= percentage <= 1:
        return 'rgb(255, 173, 92)'
    if percentage > 0:
        green_intensity = min(int((percentage / 100) * 175)+50, 175)
        return f'rgb(0, {green_intensity}, 0)'
    else:
        red_intensity = min(int((abs(percentage) / 35) * 200)+75, 200)
        return f'rgb({red_intensity}, 0, 0)'

if __name__ == "__main__":
    recipient_email = os.getenv("RECIPIENT_EMAIL")
    
    # Read the highlighted stocks data from the JSON file
    with open('highlighted_stocks.json', 'r') as json_file:
        data = json.load(json_file)
        highlighted_stocks = data['highlighted_stocks']
        stock_performance = data['stock_performance']
    
    # Call send_email with preview=True to generate a preview HTML file
    #send_email(highlighted_stocks, stock_performance, recipient_email, preview=True)

    # To send the email, change preview to False
    send_email(highlighted_stocks, stock_performance, recipient_email, preview=False)
