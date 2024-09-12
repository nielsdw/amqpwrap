from environs import Env
import pika
import ssl

env = Env()
try:
    env.read_env()
    print("Using environment variables from .env file.")
except FileNotFoundError:
    print("No .env file found. Using default environment variables.")

ca_cert = env.str("CA_CERT")
ssl_context = ssl.create_default_context(cafile=ca_cert)
ssl_options = pika.SSLOptions(ssl_context, env.str("AMQP_HOST"))
credentials = pika.PlainCredentials(env.str("AMQP_USERNAME"), env.str("AMQP_PASSWORD"))

parameters = pika.ConnectionParameters(host=env.str("AMQP_HOST"),
                                       port=5671,
                                       virtual_host=env.str("AMQP_VHOST"),
                                       credentials=credentials,
                                       ssl_options=ssl_options)
