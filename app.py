import logging
import os
import smtplib

from dotenv import load_dotenv

# Initialize env variables
load_dotenv()

# Initialize logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Get the host credentials
SENDER_MAIL = os.getenv("HOST_EMAIL")
SENDER_MAIL_PASSWORD = os.getenv("HOST_EMAIL_APP_PASSWORD")


class SendMail:
    """Mail utils class to connect the user to the SMTP server and allows to sends the mail."""

    SMTP_SERVER_DOMAIN = "smtp.gmail.com"
    SMTP_SERVER_PORT = 587

    def __init__(self, sender_email, sender_email_password) -> None:
        """Constructor to initializes the params."""

        # Initialize the sender credentials
        self.sender_email = sender_email
        self.sender_email_password = sender_email_password
        self.server = None

        # To check if user is already logged in
        self.code = None

    def is_authenticated(self):
        if self.code in (235, 503):
            return True
        return False

    def quit_server(self):
        """Function that closes the server."""

        # Close the server if it is still opens
        if self.server:
            self.server.quit()
            self.code = None
            logger.info("Closed the smtp server!")

    def mail_login(self):
        """Function to login to the mail"""

        try:
            # Establish a secure connection with the SMTP server
            logger.info("Establishing a connection to the smtp server...")
            self.server = smtplib.SMTP(
                SendMail.SMTP_SERVER_DOMAIN, SendMail.SMTP_SERVER_PORT
            )

            logger.info("Adding TLS Layer...")
            self.server.starttls()

            logger.info("Login to gmail...")
            code, resp = self.server.login(
                self.sender_email, self.sender_email_password
            )
            self.code = code

        except Exception as e:
            if self.server is not None:
                self.quit_server()
                self.server = None
                self.code = None

            logger.error(f"Error occurred while login and error is {str(e)}!")

    def send_mail(self, subject, body, receiver_email):
        """Function to send the mail to the receiver email address."""

        if self.server is not None:
            # Create the email message
            message = f"Subject: {subject}\n\n{body}"

            try:
                # Send the email
                logger.info("Sending message...")
                self.server.sendmail(
                    from_addr=self.sender_email, to_addrs=receiver_email, msg=message
                )
                logger.info("Email sent successfully!")

            except Exception as e:
                logger.error(
                    f"Error occured while sending an email and error is {str(e)}!"
                )

        else:
            logger.info(f"Email: {self.sender_email} is not logged in yet!")


if __name__ == "__main__":
    receiver_email = "youremail@example.com"
    subject = "Test Email"
    body = "Test email send from Python."

    email_obj = SendMail(SENDER_MAIL, SENDER_MAIL_PASSWORD)
    email_obj.mail_login()
    email_obj.send_mail(subject, body, receiver_email)
    email_obj.quit_server()
