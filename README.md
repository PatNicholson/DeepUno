You'll need the package "wxpython" in order to run the GUI

Run the game via the command "pythonw unogame.py <opponent type>"
  where opponent can be set to "DT" for decision tree player, "V2"
  for second heuristic player, or "Random" for random player
  
Train neural networks by running "python reinforce_nn_train.py". You can
make modifications to the architecture, optimizer and training heuristic used within the file.
You can modify "reinforce_nn.py" to make changes to the labels used for learning.

Test neural networks by setting "training" to "False" in "reinforce_nn_train.py", and
then running "python reinforce_nn_train.py"
