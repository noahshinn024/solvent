from solvent import data

DATA_FILE = 'new-data.json'
NSTRUCTURES = 10
BATCH_SIZE = 1
SPLIT = 0.9

ds = data.EnergyForceDataset(
    json_file=DATA_FILE,
    nstructures=NSTRUCTURES,
    one_hot_key={
        'H': [1., 0., 0.],
        'C': [0., 1., 0.],
        'O': [0., 0., 1.]
    },
    units='kcal')
ds.load()

mean_energy = ds.get_energy_mean()
rms_force = ds.get_force_rms()
ds.to_target_energy(shift_factor=mean_energy, scale_factor = 1 / rms_force)
ds.to_target_force(scale_factor = 1 / rms_force)

train_loader, test_loader = ds.gen_dataloaders(
    split=SPLIT,
    batch_size=BATCH_SIZE,
    should_shuffle=True
)

print('train loader')
for structure in train_loader:
    print(structure)

print('test loader')
for structure in test_loader:
    print(structure)
