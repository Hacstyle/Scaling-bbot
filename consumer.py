import pika
import subprocess

# Riceve messaggi dalla coda RabbitMQ, un messaggio alla volta
def receive_message(host, port, queue_name, username, password):
    credentials = pika.PlainCredentials(username, password)
    parameters = pika.ConnectionParameters(host, port, credentials=credentials)

    try:
        connection = pika.BlockingConnection(parameters) # Tenta di stabilire una connessione bloccante a RabbitMQ

        channel = connection.channel() # Crea un canale di comunicazione
        channel.queue_declare(queue=queue_name)

        def callback(ch, method, properties, body):
            command = body.decode() # Decodifica il messaggio ricevuto (il comando)
            print(f" [x] Comando ricevuto: '{command}'")
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True) # Esegue il comando tramite subprocess
                print(" [x] Output del comando:")
                print(result.stdout)
                if result.stderr:
                    print(" [x] Errori del comando:")
                    print(result.stderr)
                print(" [x] Comando eseguito con successo")

            except subprocess.CalledProcessError as e:
                print(f" [x] Errore durante l'esecuzione del comando: {e}")
                print(f" [x] Output dell'errore: {e.stderr}")
            except FileNotFoundError:
                print(f" [x] Comando non trovato: {command}")
            except Exception as e:
                print(f" [x] Errore inaspettato durante l'esecuzione del comando: {e}")

            print(" [x] Fatto")
            ch.basic_ack(delivery_tag=method.delivery_tag) # Conferma la ricezione del messaggio

        channel.basic_qos(prefetch_count=1) # Imposta il prefetch count a 1 per ricevere un messaggio alla volta
        channel.basic_consume(queue=queue_name, on_message_callback=callback) # Configura il consumer per utilizzare la funzione di callback

        print(' [*] In attesa di messaggi. Per uscire premi CTRL+C')
        channel.start_consuming()
    except Exception as e:
        print(f"Errore di connessione: {e}")

if __name__ == "__main__":
    rabbitmq_host = '10.99.163.146'
    rabbit_port = 5672 
    rabbitmq_queue = 'command-queue'
    rabbitmq_username = 'user'
    rabbitmq_password = 'password'

    receive_message(rabbitmq_host, rabbit_port, rabbitmq_queue, rabbitmq_username, rabbitmq_password)