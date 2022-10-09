from solvent import models, train, data

DATA_FILE = 'new-data.json'
NSTRUCTURES = 10
BATCH_SIZE = 1
SPLIT = 0.9

NATOMS = 51
NSTATES = 3


# load dataset from json
ds = data.EnergyForceDataset(DATA_FILE, nstructures=NSTRUCTURES, units='kcal')
ds.load()

# compute constants for target data shifting and scaling
mean_energy = ds.get_energy_mean()
rms_force = ds.get_force_rms()
ds.to_target_energy(shift_factor=mean_energy, scale_factor = 1 / rms_force)
ds.to_target_force(scale_factor = 1 / rms_force)

# train and test loaders
train_loader, test_loader = ds.gen_dataloaders(
    split=SPLIT,
    batch_size=BATCH_SIZE,
    should_shuffle=True
)

# initialize model
model = models.Model(
    irreps_in=f'{NATOMS}x0e',
    hidden_sizes=[125, 40, 25, 15],
    irreps_out=f'{NSTATES}x0e',
    nlayers=3,
    max_radius=4.6,
    nbasis_funcs=8,
    nradial_layers=2,
    nradial_neurons=128,
    navg_neighbors=16.0,
    cache=None
)

# initialize trainer
trainer = train.Trainer(
    model=model,
    train_loader=train_loader,
    test_loader=test_loader,
    energy_contribution=1.0,
    force_contribution=25.0,
    description='test run'
)

# run training
trainer.fit()
