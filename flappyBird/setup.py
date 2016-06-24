# =============================================================================
# =================================== GAME ====================================
# =============================================================================
WIN_BACKGROUND_SIZE = 284
WIN_WIDTH = WIN_BACKGROUND_SIZE * 3
WIN_HEIGHT = 512


BIRD_ANIMATE = 10
PIPE_ANIMATE = 5

GRAVITY = 2.5

JUMP_TIME = -GRAVITY * 4

SLEEP_TIME = 10

PASS_X = 10

PIPE_SPACE = 32
# -----------------------------------------------------------------------------


# =============================================================================
# ================================ INDIVIDUAL =================================
# =============================================================================
SIGMA_MIN = 0.0001

SIGMA_MAX = 5

NUM_GAMEPLAYS = 3

# === Mutation ===
# (1) Uncorrelated Mutations with 1 Step Size
# (2) Uncorrelated Mutations with Multiple Step Sizes
# (3) Correlated Mutations
MUTATION_TYPE = 2
# ----------------  

# === Recombination ===
CHILD_AVERAGE = True
# ---------------------

# === Neural Network ===
NUM_INPUTS = 2

HIDDEN_LAYERS = 1

NODES_PER_LAYER = 3
# ----------------------
# -----------------------------------------------------------------------------