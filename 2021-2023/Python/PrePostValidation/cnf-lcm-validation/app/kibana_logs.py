from app.modules import *


def print_log(request_id,message,level):
    #print(type(message))
    #print('I am inside print log')
    timestamp = datetime.now().isoformat()
#    request_id=data["request_id"]

    if isinstance(message, str):
        log = {
            "@timestamp": timestamp,
            "@version": "1",
            "message": message,
            "external_request_id": str(request_id),
            "level": level
        }
    elif isinstance(message, list):
        log = {
            "@timestamp": timestamp,
            "@version": '1',
            "message": ', '.join(message),
            "external_request_id": str(request_id),
            "level": level
        }
    elif isinstance(message, dict):
        log = {
            "@timestamp": timestamp,
            "@version": '1',
            "message": message,
            "external_request_id": str(request_id),
            "level": level
        }
    else:
        raise ValueError("Invalid message type. Only strings or arrays are allowed.")

    log = json.dumps(log)
    print(log)
    #print(type(log))


# Example usage
#order_id = 12345

#print_log(message)
#print_log(request_id, message_string)
#print_log(request_id, message_array)