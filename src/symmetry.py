class Symmetry(object):
    SYMMETRY_FUNCTIONS = \
    (
        lambda r,c: (r,c),     # Original
        lambda r,c: (2-c,r),   # Rotate by 90 degrees
        lambda r,c: (2-r,2-c), # Rotate by 180 degrees
        lambda r,c: (c,2-r),   # Rotate by 270 degrees
        lambda r,c: (2-r,c),   # Reflect horizontally
        lambda r,c: (r,2-c),   # Reflect vertically
        lambda r,c: (c,r),     # Reflect left diagonal
        lambda r,c: (2-c,2-r)  # Reflect right diagonal
    )

    def get_symmetries(self, state):
        for symmetry_function in self.SYMMETRY_FUNCTIONS:
            yield self._transform(symmetry_function, state)

    def _transform(self, symmetry_function, state):
        new_state = [None]*9
        for row in range(3):
            for col in range(3):
                new_row, new_col = symmetry_function(row, col)
                new_state[3*new_row+new_col] = state[3*row+col]
        return tuple(new_state)
