import pika

def send_message(host, port, queue_name, message, username, password):
    """Invia un messaggio alla coda RabbitMQ."""
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, credentials=credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(f" [x] Inviato '{message}'")

    connection.close()

if __name__ == "__main__":
    rabbitmq_host = '127.0.0.1' # Indirizzo RabbitMQ
    rabbitmq_port = 5672
    rabbitmq_queue = 'command-queue' # Nome della coda
    rabbitmq_username = 'user' # Utente RabbitMQ
    rabbitmq_password = 'password' # Password RabbitMQ
    message_to_send = input("scansione bbot da eseguire:") # Messaggio da inviare

    send_message(rabbitmq_host, rabbitmq_port, rabbitmq_queue, message_to_send, rabbitmq_username, rabbitmq_password)