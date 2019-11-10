from argparse import ArgumentParser

from dnry.config import IConfigSource, IConfigSection, IConfigFactory
from dnry.config.arg import ArgumentSource
from dnry.config.delegate import DelegateSource
from dnry.config.yaml import YamlSource
from dnry.config.environ import EnvironmentSource


class ConfigSource(IConfigSource):
    def load(self, fact: IConfigFactory, conf: IConfigSection) -> dict:

        # This delegate is called when the configuration is built
        def delegate_load(delegate_fact: IConfigFactory, delegate_conf: IConfigSection):

            if conf.has("config"):
                # User overrides configuration
                delegate_fact.add_source(YamlSource(conf.get("config")))
            else:
                # Default configuration files if user didn't specify
                delegate_fact.add_source(YamlSource([
                    "./gcmon.yaml",
                    "~/.config/gcmon/gcmon.yaml",
                    "/etc/gcmon/gcmon.yaml",
                ]))

            # Allow environment variables override config files
            delegate_fact.add_source(EnvironmentSource("GCMON_"))

            # Commandline overrides win everything - they where already parsed.
            # Adding it here will push it to the highest priority.
            delegate_fact.add_configuration(delegate_conf)

        # Setup commandline arguments and add as a configuration source.
        ap = ArgumentParser(description="Google Cast Monitor")
        ap.add_argument("-c", "--config", help="Identify a configuration file.")
        ap.add_argument("--MessageBroker:Type", help="Identify the message broker type.")

        # Add a configuration delegate to load the remaining configs.
        fact.add_source(DelegateSource(delegate_load))

        # Return the argparser object as a ArgumentSource
        return ArgumentSource(ap).load(fact, conf)
