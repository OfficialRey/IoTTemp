from datetime import datetime


def print_debug(value: str):
    print(f"| -- DEBUG -- | ({datetime.now().strftime('%d/%m/%Y @ %H:%M:%S')}): {value}")
