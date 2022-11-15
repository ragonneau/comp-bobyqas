from profiles import Profiles

if __name__ == '__main__':
    profiles = Profiles(1, 10, 'bounds')
    profiles(['bobyqa', 'py-bobyqa'])
    del profiles

    profiles = Profiles(1, 10, 'bounds', 'noisy')
    profiles(['bobyqa', 'py-bobyqa'])
    del profiles

    profiles = Profiles(1, 50, 'bounds')
    profiles(['bobyqa', 'py-bobyqa'])
    del profiles

    profiles = Profiles(1, 50, 'bounds', 'noisy')
    profiles(['bobyqa', 'py-bobyqa'])
    del profiles
