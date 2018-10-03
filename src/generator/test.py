from generator.base import Commander
from utils.common import abs_path


def main():
    commander = Commander('/Users/antoni.mleczko/tmp/output')

    commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script0'))
    commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script1'))
    commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script2'))

    commander.execute()


if __name__ == "__main__":
    main()
