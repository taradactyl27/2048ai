# 2048ai - Alex Taradachuk

I used expecitmax with weighted heuristics for my approach to the problem. For heuristics I used a weighted dot product, with a snake matrix, smoothness, and free cells. After playing around with multiple weights, I found the best performance to be given by default values with certain weights applied during evaluation.