import logging
import queue
import random
import string
import time

import attr

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

@attr.s
class PubSubMessage:
    instance_name = attr.ib()
    message_id    = attr.ib(repr=False)
    hostname      = attr.ib(repr=False, init=False)

    def __attrs_post_init__(self):
        self.hostname = f"{self.instance_name}.example.net"


def publish(queue, n):
    choices = string.ascii_lowercase + string.digits
    for x in range(1, n + 1):
        host_id = "".join(random.choices(choices, k=4))
        instance_name = f"cattle-{host_id}"
        msg = PubSubMessage(message_id=x, instance_name=instance_name)
        # publish an item
        queue.put(msg)
        logging.info(f"Published {x} of {n} messages")

    # indicate the publisher is done
    queue.put(None)


def consume(queue):
    while True:
        # wait for an item from the publisher
        msg = queue.get()

        # the publisher emits None to indicate that it is done
        if msg is None:
            break

        # process the msg
        logging.info(f'Consumed {msg}')
        # simulate i/o operation using sleep
        time.sleep(random.random())


def main():
    start_time = time.time()

    line = queue.Queue()
    publish(line, 5)
    consume(line)

    duration = time.time() - start_time

    logging.info(f'Successfully shutdown the Mayhem service after {duration} seconds.')



if __name__ == "__main__":
    main()
