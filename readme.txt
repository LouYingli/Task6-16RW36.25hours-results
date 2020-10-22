1.add models in the SourceFolder 
ASHRAEModel(1PrepareASHRAEModel\2Operation\calibratedModel),
bEQModel_post (post-1980\2Operation\calibratedModel), 
bEQModel_pre (Pre-1980\2Operation\calibratedModel)
2.modify main.py
num_sens
min_value
max_value
ASHRAEModel_schedule
bEQ_schedule
3.parallelSimuMeta need to be modified if the PDF is not PLD
4.run main.py