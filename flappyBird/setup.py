# =============================================================================
# =================================== GAME ====================================
# =============================================================================

WIN_BACKGROUND_SIZE = 284

WIN_WIDTH = WIN_BACKGROUND_SIZE * 3

WIN_HEIGHT = 512

BIRD_ANIMATE = 10

# PIPE_ANIMATE = 3 seems to be a good value
PIPE_ANIMATE = 3

GRAVITY = 2.5

# JUMP_TIME = -GRAVITY * 2 seems to be a good value
JUMP_TIME = -GRAVITY * 2

SLEEP_TIME = 10

PASS_X = 10

PIPE_SPACE = 32

# -----------------------------------------------------------------------------


# =============================================================================
# ========================== EVOLUTIONARY STRATEGY ============================
# =============================================================================

MAX_ITERATIONS = 25

TARGET_SCORE = 100

GENERATIONAL = True

POPULATION_SIZE = 10

CHILDREN_POP_RATIO = 7

PARENT_SELECTION_FN = "global_uniform_selection"

SURVIVOR_SELECTION_FN = "heap_survivor_selection"

# === Mutation ===
NUM_MUTATION_TRIALS = 3

MUTATION_FN = "multiple_sd"

SIGMA_MIN = 0.0001

SIGMA_MAX = 1

# (1) Uncorrelated Mutations with 1 Step Size
# (2) Uncorrelated Mutations with Multiple Step Sizes
# (3) Correlated Mutations
MUTATION_TYPE = 2

# === Recombination ===
RECOMBINATION_FN = "hibrid_recomb"

CHILD_AVERAGE = True
# ---------------------

# === Fitness ===
NUM_GAMEPLAYS = 3
# ---------------

# -----------------------------------------------------------------------------



# =============================================================================
# ============================== NEURAL NETWORK ===============================
# =============================================================================

NUM_INPUTS = 6

HIDDEN_LAYERS = 1

NODES_PER_LAYER = 10

# -----------------------------------------------------------------------------