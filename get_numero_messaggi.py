import pika

def get_queue_message_count(host, port, queue_name, username, password):
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    queue_info = channel.queue_declare(queue=queue_name, passive=True)
    message_count = queue_info.method.message_count

    connection.close()
    return message_count

# Esempio di utilizzo:
message_count = get_queue_message_count('127.0.0.1', 5672, 'command-queue', 'user', 'password')
print(f"Numero di messaggi nella coda: {message_count}")