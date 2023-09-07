from datetime import datetime
from pytz import timezone

def chile_time():
    scl = timezone('America/Santiago')
    scl_time = datetime.now(scl).strftime('%Y-%m-%dT%H-%M-%S')
    return scl_time
