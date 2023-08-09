import fire

from wedne.client.__main__ import sync_main as client_main

if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write(  # type: ignore
        "\n".join(lines) + "\n",
    )
    fire.Fire(client_main, name="wedne")
