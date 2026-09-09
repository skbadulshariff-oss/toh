class TowerOfHanoiAI:
    def __init__(self):
        self.moves = []

    def get_solution(self, n, source=0, target=2, auxiliary=1):
        self.moves = []
        self._solve(n, source, target, auxiliary)
        return self.moves

    def _solve(self, n, source, target, auxiliary):
        if n > 0:
            # Move n-1 disks from source to auxiliary
            self._solve(n - 1, source, auxiliary, target)
            # Move bottom disk to target
            self.moves.append((source, target))
            # Move n-1 disks from auxiliary to target
            self._solve(n - 1, auxiliary, target, source)
