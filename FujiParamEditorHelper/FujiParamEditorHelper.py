import numpy as np
import pandas as pd


def read_pac_file(pac_file):
    """
    read data from .PAC file from FujiParaEditor.exe
    :param pac_file: string
    :return: nsamps, samp_dur, baseline, df
    """
    with open(pac_file, 'r') as f:
        for _ in range(6):
            next(f)
        nsamps = np.int(f.readline())

        for _ in range(2):
            next(f)
        baseline = np.double(f.readline().strip())
        samp_dur = np.double(f.readline().strip())

    df = pd.read_csv(pac_file, delim_whitespace=True, skiprows=20, names=('T1', 'T2', 'A', 'param'))

    return nsamps, samp_dur, baseline, df

def get_accent_contour(pac_file):
    """
    calculate accent curve from .PAC file, output from FujiParaEditor.exe
    :param pac_file: string
    :return: phrase_contour
    """
    nsamps, samp_dur, baseline, df = read_pac_file(pac_file)
    tmax = nsamps * samp_dur

    fs = 400
    accent_contour = np.zeros(int(tmax * fs))

    for i, row in df.iloc[np.where(df['param'] == 20)].iterrows():
        beta = row['param']
        T =    row['T1']
        dur =  row['T2'] - T
        A =    row['A']

        accent_contour = accent_contour + A * Ga2(beta, T, dur, tmax=tmax, fs=fs)

    return accent_contour


def get_phrase_contour(pac_file):
    """
    calculate phrase curve from .PAC file, output from FujiParaEditor.exe
    :param pac_file: string
    :return: phrase_contour
    """
    nsamps, samp_dur, baseline, df = read_pac_file(pac_file)
    tmax = nsamps * samp_dur

    fs = 400
    phrase_contour = np.zeros(int(tmax * fs))

    for i, row in df.iloc[np.where(df['param'] == 2)].iterrows():
        alpha = row['param']
        T = row['T1']
        A = row['A']

        phrase_contour = phrase_contour + A * Gp(alpha, T, tmax=tmax, fs=fs)

    return phrase_contour


def get_baseline(pac_file):
    return read_pac_file(pac_file)[2]


def write_f0_ascii(pitch, tt_pitch, fname):
    """
    Extract a pitch contour for a sentence and save it in a file format that is accepted by FujiParamEditor
    :param pitch:
    :param tt_pitch:
    :param praat:
    :return:
    """

    df = pd.DataFrame()
    df['1'] = pitch
    df['2'] = np.double(~np.isnan(pitch))
    df['3'] = 1.0
    df['4'] = df['2']
    df['1'][np.isnan(df['1'])] = 0.0

    df.to_csv(fname, header=False, index=False, sep=' ')


def read_f0_ascii(f0_ascii_file):
    """
    reads f0 file that is in the format taken by FujiParamEditor
    :param f0_ascii_file: filepath
    :return: pitch, tt_pitch, dt
    """
    df = pd.read_csv(f0_ascii_file, names=('pitch', 'voiced', 'na', 'na'), sep=' ')
    pitch = df['pitch'].values
    pitch[np.logical_not(pitch)] = np.nan
    tt_pitch = np.arange(len(pitch)) / 100

    return pitch, tt_pitch, .01


def fuji2pitch(baseline, accent, phrase):
    """
    Get reconstruction of pitch contour from fujisaki components
    :param baseline: float. Use get_baseline(pac_file)
    :param accent: np.array. Use get_accent_contour(pac_file)
    :param phrase: np.array. Use get_phrase_contour(pac_file)
    :return: np.array
    """
    logpitch = accent + np.log(baseline) + phrase
    pitch = np.exp(logpitch)

    return pitch


# functions of the components of the Fujisaki model
def Ga_func(beta, tt, gamma=np.inf):
    val = 1 - (1 + beta * tt) * np.exp(-beta * tt)
    val[val > gamma] = gamma
    return val


def Ga(beta, T, tmax=2, fs=400):
    val = np.zeros(int(tmax * fs))
    trange = np.arange(0, tmax, 1/fs)[:len(val)]
    func_domain = trange - T >= 0
    val[func_domain] = Ga_func(beta, trange[func_domain] - T)
    return val


def Ga2(beta, T, dur, tmax=3, fs=400):
    return Ga(beta, T, tmax=tmax, fs=fs) - Ga(beta, T + dur, tmax=tmax, fs=fs)


def Gp_func(alpha, tt):
    return (alpha ** 2) * np.exp(-alpha * tt) * tt


def Gp(alpha, T, tmax=2, fs=400):
    val = np.zeros(int(tmax * fs))
    trange = np.arange(0, tmax, 1/fs)[:len(val)]
    func_domain = trange - T >= 0
    val[func_domain] = Gp_func(alpha, trange[func_domain] - T)
    return val

