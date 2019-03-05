from generator import Commander, GeneratorStateMaster


def make_generator_entry(caption, state):
    """
    Convenience function used to return one option 'row' using the caption and state append action
    (the common operation)

    :param caption: string to be used as an action's caption
    :param state: state to be appended to state_chain in action
    :return:
    """
    return {
        'caption': caption,
        'action': lambda: GeneratorStateMaster().append_state(state),
    }


def make_pop_entry():
    """
    Convenience function for generating common action which is popping state
    """
    return {
        'caption': COMMON_CAPTIONS['back'],
        'action': lambda: GeneratorStateMaster().pop_state(),
    }


def make_execute_entry():
    """
    Convenience function for generating common action which is accepting and executing commands in command chain
    """
    return {
        'caption': COMMON_CAPTIONS['accept'],
        'action': lambda: Commander().execute(),
    }


COMMON_CAPTIONS = {
    'back': 'Back',
    'accept': 'Accept',
}