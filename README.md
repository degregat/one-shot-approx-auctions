# Differentially Private Approximately Optimal Auctions through Deep Learning
Fork of [Optimal Auctions through Deep Learning](https://github.com/saisrivatsan/deep-opt-auctions) (https://arxiv.org/pdf/1706.03459.pdf), using [TensorFlow Privacy](https://github.com/tensorflow/privacy/) to make the RegretNet approach Differentially Private, resulting in Approximate Truthfulness and Collusion Resistance in the sense of “Mechanism Design via Differential Privacy" (Frank McSherry and Kunal Talwar, In FOCS, pages 94–103, 2007). This means we can relax the assumption of having prior knowledge of the valuation profiles.

The outer loop of the lagrange optimizer (see Section 4 of the [paper on "Optimal Auctions through Deep Learning"](https://arxiv.org/pdf/1706.03459.pdf)) in this fork is differentially private, bounding the rate of change of the lagrange multipliers on the regret per agent. Therefore, the influence each agent has on the resulting allocation and payment functions is bounded.

## MPC Federated Learning with tf-encrypted
For now, MPC happens offline, using processes for agent separation. It averages aggregated lagrangian updates from full local simulations, using the [pond protocol](https://github.com/tf-encrypted/tf-encrypted/blob/master/tf_encrypted/protocol/pond/pond.py) of [TF Encrypted](https://github.com/tf-encrypted/tf-encrypted). It loosely follows the [federated learning](https://github.com/tf-encrypted/tf-encrypted/tree/master/examples/federated-learning) example, with the difference of directly using the compute_gradients and apply_gradients functions of the optimizer. This way TF Privacy can be used directly. In this iteration, the assumption still is that agents submit gradients, during the computation of which they have applied noise and clipping correctly. The main improvement is increased confidentiality.

#### Next steps
- port to TF2.0
- agentwise simulation and aggregation of all necessary model parameters
- networking and async orchestration
- distribute application of noise and clipping to reduce trust needed in agents

## Examples

Here you can see annotated example notebooks of the settings: 
- [additive_1x2_uniform](https://github.com/degregat/deep-opt-auctions/blob/exp_comparison_dp_no_dp_additive_1x2_uniform/regretNet/batch_experiments/additive_1x2_uniform_batch_1/visualize_additive_1x2_uniform_batch_1.ipynb) with differential privacy, no MPC aggregation
- [additive_5x10_uniform](https://github.com/degregat/deep-opt-auctions/blob/exp_comparison_dp_no_dp_additive_5x10_uniform/regretNet/batch_experiments/additive_5x10_uniform_batch_1/visualize_additive_5x10_uniform_batch_1.ipynb) with differential privacy, no MPC aggregation

## Getting Started

- install Python >=3.6.8
- clone this repository and `cd` into it
- install requirements with pipenv or pip (e.g. `pip3 install -r requirements.txt --user`)

## Running the experiments

### RegretNet

In `deep-opt-auctions/regretNet` execute `./run_batch.py`

Supported settings so far are `additive_1x2_uniform` and `additive_5x10_uniform`. Modifying other configs is straightforward (see:  "Parameters for differentially private optimizer" in `deep-opt-auctions/regretNet/cfgs/additive_1x2_uniform_config.py`)

Example:
`./run_batch.py --setting additive_5x10_uniform --noise-vals 0.001 0.01 0.1 --clip-vals 0.1 0.5 1 --add-no-dp-run --iterations 100000`

This will create `additive_5x10_uniform_batch_1` in `batch_experiments`, which contains `visualize_additive_5x10_uniform_batch_1.ipynb` displaying the results of the runs. 

Note:
You can also have code and results commited to git. To do that, uncomment `commit_code()`, `commit_data()` and the exeption handlers in `run_batch` of `run_batch.py`.
The final model, data logs and the visualization will be commited to the branch `exp_example_1`. If you give a description, it should be unique. To examine the results, switch to the branch after the run has finished. Because of the branching during experiments, it is not advisable to do this in your development repository, or to run multiple batches in parallel. Use multiple copies of the repository instead. (Later versions might use an experiment framework to alleviate this.)

## Open Problems
- Interpretation of the results regarding robustness
- Analyze effect of and refine orders [more information here](https://github.com/tensorflow/privacy/blob/master/tutorials/walkthrough/walkthrough.md)



# Optimal Auctions through Deep Learning
Implementation of "Optimal Auctions through Deep Learning" (https://arxiv.org/pdf/1706.03459.pdf)

## Getting Started

Install the following packages:
- Python 2.7 
- Tensorflow
- Numpy and Matplotlib packages
- Easydict - `pip install easydict`

## Running the experiments

### RegretNet

#### For Gradient-Based approach:
Default hyperparameters are specified in regretNet/cfgs/.  

#### For Sample-Based approach:
Modify the following hyperparameters in the config file specified in regretNet/cfg/.
```
cfg.train.gd_iter = 0
cfg.train.num_misreports = 100
cfg.val.num_misreports = 100 # Number of val-misreports is always equal to the number of train-misreports
```

For training the network, testing the mechanism learnt and computing the baselines, run:
```
cd regretNet
python run_train.py [setting_name]
python run_test.py [setting_name]
python run_baseline.py [setting_name]
```

setting\_no  |      setting\_name |
 :---:   | :---: |
  (a)    |  additive\_1x2\_uniform |
  (b)   | unit\_1x2\_uniform\_23 |
  (c\)  | additive\_2x2\_uniform |
  (d)   | CA\_sym\_uniform\_12 |
  (e)    | CA\_asym\_uniform\_12\_15 |
  (f)   | additive\_3x10\_uniform |
  (g)  | additive\_5x10\_uniform |
  (h) |   additive\_1x2\_uniform\_416\_47
  (i) |   additive\_1x2\_uniform\_triangle
  (j) |   unit\_1x2\_uniform
  (k) |  additive\_1x10\_uniform
  (l) |   additive\_1x2\_uniform\_04\_03
  (m) |   unit\_2x2\_uniform


### RochetNet (Single Bidder Auctions)

Default hyperparameters are specified in rochetNet/cfgs/.  
For training the network, testing the mechanism learnt and computing the baselines, run:
```
cd rochetNet
python run_train.py [setting_name]
python run_test.py [setting_name]
python run_baseline.py [setting_name]
```
setting\_no  |      setting\_name |
 :---:  | :---: |
  (a)   |  additive\_1x2\_uniform |
  (b)   |   additive\_1x2\_uniform\_416\_47
  \(c\) |   additive\_1x2\_uniform\_triangle
  (d)   |   additive\_1x2\_uniform\_04\_03
  (e)   |  additive\_1x10\_uniform
  (f)   |   unit\_1x2\_uniform
  (g)   |   unit\_1x2\_uniform\_23
  
### MyersonNet (Single Item Auctions)
  
Default hyperparameters are specified in utils/cfg.py.  
For training the network, testing the mechanism learnt and computing the baselines, run:
```
cd myersonNet
python main.py -distr [setting_name] or
bash myerson.sh
```
setting\_no  |      setting\_name |
 :---:  | :---: |
  (a)   |  exponential 
  (b)   |   uniform
  \(c\) |   asymmetric\_uniform 
  (d)   |   irregular

 
## Settings

### Single Bidder
- **additive\_1x2\_uniform**: A single bidder with additive valuations over two items, where the items is drawn from U\[0, 1\].

- **unit\_1x2\_uniform\_23**: A single bidder with unit-demand valuations over two items, where the item values are drawn from U\[2, 3\].

- **additive\_1x2\_uniform\_416\_47**: Single additive bidder with preferences over two non-identically distributed items, where v<sub>1</sub> ∼ U\[4, 16\]and v<sub>2</sub> ∼ U\[4, 7\].

- **additive\_1x2\_uniform\_triangle**: A single additive bidder with preferences over two items, where (v<sub>1</sub>, v<sub>2</sub>) are drawn jointly and uniformly from a unit-triangle with vertices (0, 0), (0, 1) and (1, 0).

- **unit\_1x2\_uniform**: A single unit-demand bidder with preferences over two items, where the item values from U\[0, 1\]

- **additive\_1x2\_uniform\_04\_03**: A Single additive bidder with preferences over two items, where the item values v<sub>1</sub> ∼ U\[0, 4], v<sub>2</sub> ∼ U\[0, 3]

- **additive\_1x10\_uniform**: A single additive bidder and 10 items, where bidders draw their value for each item from U\[0, 1\].

### Multiple Bidders
- **additive\_2x2\_uniform**: Two additive bidders and two items, where bidders draw their value for each item from U\[0, 1\]. 

- **unit\_2x2\_uniform**: Two unit-demand bidders and two items, where the bidders draw their value for each item from identical U\[0, 1\].

- **additive\_2x3\_uniform**: Two additive bidders and three items, where bidders draw their value for each item from U\[0, 1\]. 

- **CA\_sym\_uniform\_12**: Two bidders and two items, with v<sub>1,1</sub>, v<sub>1,2</sub>, v<sub>2,1</sub>, v<sub>2,2</sub> ∼ U\[1, 2\], v<sub>1,{1,2}</sub> = v<sub>1,1</sub> + v<sub>1,2</sub> + C<sub>1</sub> and v<sub>2,{1,2}</sub> = v<sub>2,1</sub> + v<sub>2,2</sub> + C<sub>2</sub>, where C<sub>1</sub>, C<sub>2</sub> ∼ U\[−1, 1\].

- **CA\_asym\_uniform\_12\_15**: Two bidders and two items, with v<sub>1,1</sub>, v<sub>1,2</sub> ∼ U\[1, 2\], v<sub>2,1</sub>, v<sub>2,2</sub> ∼ U\[1, 5\], v<sub>1,{1,2}</sub> = v<sub>1,1</sub> + v<sub>1,2</sub> + C<sub>1</sub> and v<sub>2,{1,2}</sub> = v<sub>2,1</sub> + v<sub>2,2</sub> + C<sub>2</sub>, where C<sub>1</sub>, C<sub>2</sub> ∼ U\[−1, 1].

- **additive\_3x10\_uniform**: 3 additive bidders and 10 items, where bidders draw their value for each item from U\[0, 1\].

- **additive\_5x10\_uniform**: 5 additive bidders and 10 items, where bidders draw their value for each item from U\[0, 1\].


## Visualization

Allocation Probabilty plots for **unit\_1x2\_uniform_23** setting learnt by **regretNet**:

<img src="https://github.com/saisrivatsan/deep-opt-auctions/blob/master/regretNet/plots/visualization/unit_1x2_uniform_23_alloc1.png" width="300"> <img src="https://github.com/saisrivatsan/deep-opt-auctions/blob/master/regretNet/plots/visualization/unit_1x2_uniform_23_alloc2.png" width="300">

Allocation Probabilty plots for **additive\_1x2\_uniform\_416\_47** setting learnt by **rochetNet**:

<img src="https://github.com/saisrivatsan/deep-opt-auctions/blob/master/rochetNet/plots/visualization/additive_1x2_uniform_416_47_alloc1.png" width="300"> <img src="https://github.com/saisrivatsan/deep-opt-auctions/blob/master/rochetNet/plots/visualization/additive_1x2_uniform_416_47_alloc2.png" width="300">

For other allocation probability plots, check-out the ipython notebooks in `regretNet` or `rochetNet` folder.


## Reference

Please cite our work if you find our code/paper is useful to your work.
```
@article{DFNP19,
  author    = {Paul D{\"{u}}tting and Zhe Feng and Harikrishna Narasimhan and David C. Parkes and Sai Srivatsa Ravindranath},
  title     = {Optimal Auctions through Deep Learning},
  journal   = {arXiv preprint arXiv:1706.03459},
  year      = {2019},
}
```
