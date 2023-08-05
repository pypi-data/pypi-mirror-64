import snakypy
from zshpower import decorators
from zshpower.zshpower import ZSHPower

zshpower_ = ZSHPower()


@decorators.assign_cli(zshpower_.arguments, "init")
def init():
    zshpower_.init_command()


@decorators.assign_cli(zshpower_.arguments, "config")
def config_action():
    zshpower_.config_command()


@decorators.checking_init_command(zshpower_.themes_folder)
@decorators.assign_cli(zshpower_.arguments, "enable")
def enable():
    zshpower_.enable_command()


@decorators.assign_cli(zshpower_.arguments, "disable")
def disable():
    zshpower_.disable_command(zshpower_.arguments)


@decorators.assign_cli(zshpower_.arguments, "--credits")
def credence():
    zshpower_.credence_command()


@decorators.assign_cli(zshpower_.arguments, "reload")
def reload_config():
    zshpower_.reload_command()


@decorators.assign_cli(zshpower_.arguments, "reset")
def reset_config():
    zshpower_.reset_command()


@decorators.assign_cli(zshpower_.arguments, "uninstall")
def uninstall():
    zshpower_.uninstall_command()


@snakypy.decorators.denying_os("nt")
def main():
    (
        init(),
        enable(),
        disable(),
        credence(),
        uninstall(),
        config_action(),
        reset_config(),
        reload_config(),
    )
