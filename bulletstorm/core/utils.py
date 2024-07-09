import logging, os


class ModuleNameFormatter(logging.Formatter):
    def format(self, record):
        record.module = record.module.split(".")[-1]
        return super(ModuleNameFormatter, self).format(record)


def setup_logging(name=None):
    if not logging.root.handlers:
        logging.basicConfig(
            level=logging.ERROR,
            format="%(levelname).1s|%(module)12.12s:%(lineno)d|\t%(message)s",
        )

    if name is not None:
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG if os.environ.get("DEBUG") else logging.INFO)

        # Custom formatter
        formatter = ModuleNameFormatter()

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        log.handlers.clear()
        log.addHandler(console)

        return log
