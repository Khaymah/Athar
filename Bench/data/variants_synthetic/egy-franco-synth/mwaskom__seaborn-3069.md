3andi e2tera7 lel `so.Nominal` scales (w kaman elly betet3amal infer): 3ayezha tetsarraf zay el categorical axis bta3 el categorical plots fi seaborn. ya3ni 3 7agat:
1) el axis limits teb2a +/- 0.5 7awalein awel w a5er tick, msh bel margin logic el 3adi
2) mafeesh grid, 7atta law el style el shaghal biyersem grid
3) law heya 3al y axis, el axis yet3amalo invert
mola7zat: ra2am 1 sa3ba shwaya, el tari2a elly ba2tare7ha invisible artist be sticky edges w margin 0 (hacky shwaya), aw yemken sticky edges 3al spine. ra2am 2 ghaleban makanha fi `Plotter._finalize_figure`, bas lessa msh 3aref el user hay3mel force lel grid men el theme ezay, yemken el grid yet7at 3al scale. ra2am 3 sahla bas msh mot2akked makanha fein.
