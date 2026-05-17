import os
import signal
import time


running = True


def handle_shutdown(signum: int, frame: object) -> None:
    global running
    running = False
    print(f"Worker recebeu sinal {signum}. Encerrando...", flush=True)


signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)


def main() -> None:
    heartbeat_seconds = int(os.getenv("WORKER_HEARTBEAT_SECONDS", "30"))
    environment = os.getenv("APP_ENV", "local")

    print(
        f"Worker Guia Produto Radar iniciado em ambiente {environment}.",
        flush=True,
    )

    while running:
        print("Worker ativo. Nenhuma fila configurada nesta fase.", flush=True)
        time.sleep(heartbeat_seconds)

    print("Worker encerrado com sucesso.", flush=True)


if __name__ == "__main__":
    main()
