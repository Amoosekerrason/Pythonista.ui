import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="booking.log",
    filemode="w"
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(name)s: %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger(__name__).addHandler(console)
