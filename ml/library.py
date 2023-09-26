DATADIR = '../data/chess/uploaded/'
DBFNAME = 'study_p_5_5.csv'

FILTNAME = 'bp_notch_avgref.csv'

INSPECT_ICA_COMPONENTS = True

ONE_FILE = False  #"../data/chess/uploaded/06230396_35_1682376798870.2505.json"

TOLERANCE = float("2.0")  # 2 milliseconds

SAMPLING_RATE = 256
RANDOM_STATE  = 0

# Define frequency bands
# https://web.archive.org/web/20181105231756/http://developer.choosemuse.com/tools/available-data#Absolute_Band_Powers
FREQUENCY_BANDS = {'delta': (1, 4), 'theta': (4, 8), 'alpha': (7.5, 13), 'beta': (13, 30), 'gamma': (30, 44)}

CH_NAMES = ['probe-0', 'probe-1', 'probe-2', 'probe-3']
N_CHANS  = len(CH_NAMES)
