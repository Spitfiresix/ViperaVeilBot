
from viperaveil.utilities.ApiCalls import get_tt_latest_vid

def tt_lookup(id):
    data = get_tt_latest_vid(id)
    if data:
        return data
    else:
        return 'Error'