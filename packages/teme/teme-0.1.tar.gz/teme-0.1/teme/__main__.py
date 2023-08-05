import argparse
from teme.teme import get_token
from teme.teme import send_message

# construct the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--message", required=True,
    help="message to send to telegram pushit bot")
ap.add_argument("-t", "--token", required=False, default='None',
    help="pushit bot token address")
ap.add_argument("-a", "--address", required=False,
    default="https://gist.githubusercontent.com/imneonizer/90023d04d1f60d8f54e9c3b473d5b335/raw/f94843afe90b2da4a991c190e5bf5bf787a571ab/tokens.json",
    help="pushit bot token address")
args = vars(ap.parse_args())

if args["token"] == 'None':
    args["token"] = get_token(args["address"])

send_message(args["message"], args["token"])

