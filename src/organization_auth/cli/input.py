from organization_auth.cli.console import console


def warning_confirm(message: str):
    result = console.input(f":warning: {message} [y/N]", emoji=True)

    if result.lower() == "y":
        return True
    else:
        False
