# Ranger-Deep-Learning-Optimizer

Install with 
```bash
pip install pytorch_ranger
```


Ranger - a synergistic optimizer combining RAdam (Rectified Adam) and LookAhead in one codebase.

Latest version 9.3.19 - full refactoring for slow weights and one pass handling (vs two before).  Refactor should eliminate any random save/load issues regarding memory.


///////////////////////

Beta Version - Ranger913A.py:

For anyone who wants to try this out early, this version changes from RAdam to using calibrated anistropic adaptive learning rate per this paper:

https://arxiv.org/abs/1908.00700v2

"Empirical studies support our observation of the anisotropic A-LR and show that the proposed methods outperform existing AGMs and generalize even better than S-Momentum in multiple deep learning tasks."

Initial testing looks very good for training stabilization.  Any feedback in comparsion with current Ranger (9.3.19) is welcome!

/////////////////////

Medium article with more info:  
https://medium.com/@lessw/new-deep-learning-optimizer-ranger-synergistic-combination-of-radam-lookahead-for-the-best-of-2dc83f79a48d

Multiple updates:
1 - Ranger is the optimizer we used to beat the high scores for 12 different categories on the FastAI leaderboards!  (Previous records all held with AdamW optimizer).

2 - Highly recommend combining Ranger with: Mish activation function, and flat+ cosine anneal training curve.

3 - Based on that, also found .95 is better than .90 for beta1 (momentum) param (ala betas=(0.95, 0.999)).

Fixes:
1 - Differential Group learning rates now supported.  This was fix in RAdam and ported here thanks to @sholderbach.
2 - save and then load may leave first run weights stranded in memory, slowing down future runs = fixed.

### Installation
Clone the repo, cd into it and install it in editable mode (`-e` option).
That way, these is no more need to re-install the package after modification.
```bash
git clone https://github.com/lessw2020/Ranger-Deep-Learning-Optimizer
cd Ranger-Deep-Learning-Optimizer
pip install -e . 
```

### Usage 
```python
from pytorch_ranger import Ranger  # this is from ranger.py
from pytorch_ranger import RangerVA  # this is from ranger913A.py
from pytorch_ranger import RangerQH  # this is from rangerqh.py

# Define your model
model = ...
# Each of the Ranger, RangerVA, RangerQH have different parameters.
optimizer = Ranger(model.parameters(), **kwargs)
```
Usage and notebook to test are available here:
https://github.com/lessw2020/Ranger-Mish-ImageWoof-5



