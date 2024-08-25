import logging

def setup_logging():
    logging.basicConfig(
        filename="C:\\L_C_ITT\\Learn-Code_Final_Project\\module\\user_actions.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
