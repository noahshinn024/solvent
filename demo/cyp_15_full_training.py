from solvent.data import EnergyForceDataset
from solvent.models import Model
from solvent.train import Trainer

DATA_FILE = 'new-data.json'
NSTRUCTURES = 100
BATCH_SIZE = 1
SPLIT = 0.9

NATOMS = 51
NATOM_TYPES = 3
NSTATES = 3


# load dataset from json
ds = EnergyForceDataset(
    json_file=DATA_FILE,
    nstructures=NSTRUCTURES,
    one_hot_key={
        'H': [1., 0., 0.],
        'C': [0., 1., 0.],
        'O': [0., 0., 1.]
    },
    units='kcal')
ds.load()
print('loaded dataset')

# compute constants for target data shifting and scaling
mean_energy = ds.get_energy_mean()
rms_force = ds.get_force_rms()
ds.to_target_energy(shift_factor=mean_energy, scale_factor = 1 / rms_force)
ds.to_target_force(scale_factor = 1 / rms_force)
print('constants computed')

# train and test loaders
train_loader, test_loader = ds.gen_dataloaders(
    split=SPLIT,
    batch_size=BATCH_SIZE,
    should_shuffle=True
)
print('loaders')

# initialize model
model = Model(
    irreps_in=f'{NATOM_TYPES}x0e',
    hidden_sizes=[125, 40, 25, 15],
    irreps_out=f'{NSTATES}x0e',
    nlayers=4,
    max_radius=4.6,
    nbasis_funcs=8,
    nradial_layers=3,
    nradial_neurons=128,
    navg_neighbors=16.0,
    cache=None
)
print('model initialized')

# initialize trainer
trainer = Trainer(
    model=model,
    train_loader=train_loader,
    test_loader=test_loader,
    energy_contribution=1.0,
    force_contribution=25.0,
    energy_scale=rms_force,
    force_scale=rms_force,
    nmol=16,
    units='kcal/mol',
    log_dir='cyp-train',
    description='cyclopropenone in a 15 water solvent: full training'
)
print('trainer initialized')

# run training
print('running training!')
trainer.fit()
