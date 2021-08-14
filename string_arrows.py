def string_with_arrows(text, pos_start, pos_end):
    result = ''

    # Calculate indices
    ind_start = max(text.rfind('\n', 0, pos_start.ind), 0)
    ind_end = text.find('\n', ind_start + 1)
    if ind_end < 0: ind_end = len(text)
    
    # Generate each line
    line_count = pos_end.ln - pos_start.ln + 1
    for i in range(line_count):
        # Calculate line columns
        line = text[ind_start:ind_end]
        col_start = pos_start.col if i == 0 else 0
        col_end = pos_end.col if i == line_count - 1 else len(line) - 1

        # Append to result
        result += line + '\n'
        result += ' ' * col_start + '^' * (col_end - col_start)

        # Re-calculate indices
        ind_start = ind_end
        ind_end = text.find('\n', ind_start + 1)
        if ind_end < 0: ind_end = len(text)

    return result.replace('\t', '')