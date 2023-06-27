import fire

from wed.client.watcher import Watcher


class Main:
    def __call__(
        self,
        endpoint: str,
    ) -> None:
        w = Watcher(endpoint, seconds_of_delay=2, social_media_id=301)
        w()


if __name__ == "__main__":
    fire.core.Display = lambda lines, out: out.write("\n".join(lines) + "\n")  # type: ignore
    fire.Fire(Main(), name="wed.client")
