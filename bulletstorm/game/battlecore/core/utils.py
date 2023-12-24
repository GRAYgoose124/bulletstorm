def input_selection(prompt, options):
    for i, action in enumerate(options):
        if hasattr(action, "name"):
            print(f"\t{i+1}. {action.name}")
        else:
            print(f"\t{i+1}. {action}")
    selection = None
    while selection is None:
        try:
            selection = int(input(prompt))
        except ValueError:
            print("Invalid selection.")
            continue
        if selection < 1 or selection > len(options):
            print("Invalid selection.")
            selection = None

    return options[selection - 1]
