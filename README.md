# Satellites: What's the probability of being hit by a satellite?

## TO-DO
- [x] check if data is legit with different reference location
- [x] plot points in circle
- [x] plot all points with openstreetmap background (px express or something else)

- [x] cutoff coords in above_180
- [ ] investigate starlink cutoff at northpole compared to all satellites
- [ ] Kosmos vs USA

- [ ] kernel density estimation (parzen window)
  - [ ] Try different windows
  - [ ] Try different kernel functions
      - I think we can't use seaborn for that, but have to fight with sklearn.neighbors.KernelDensity and Basemap
      - maybe this helps: https://scikit-learn.org/stable/auto_examples/neighbors/plot_species_kde.html#sphx-glr-auto-examples-neighbors-plot-species-kde-py
  - [ ] discrete and continous
  - [ ] Plots 
- [x] Hypothesis testing:
  - [x] Null: Satellites are uniformly distributed vs H1: not unifromly distributed
  - We can see that already in the kde plots. No test needed
- [ ] Calculate proba of being hit in Tübingen
  - [ ] Define assumptions and simpifications (important for paper)
  - [ ] Define area, try out different area sizes
- [ ] Video of satellits ...     
