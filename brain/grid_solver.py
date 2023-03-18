import z3

def reveal_cells(hexagons):
	solver = z3.Solver()
	vars = {}

	def addVarIfMissing(r: int, q: int):
		name = f'{r}_{q}'

		if name not in vars:
			v = z3.Int(name)
			solver.add(v >= 0)
			solver.add(v <= 1)
			vars[name] = v

		return vars[name]

	def hexIs(h, value: int):
		var = addVarIfMissing(h.r, h.q)
		solver.add(var == value)

	def hexNeiSum(h, sum: int):
		dneis = [
			(+1,  0), (+1, -1), ( 0, -1),
			(-1,  0), (-1, +1), ( 0, +1)
		]
		neis = []

		for (dr, dq) in dneis:
			neis.append(addVarIfMissing(h.r + dr, h.q + dq))

		solver.add(neis[0] + neis[1] + neis[2] + neis[3] + neis[4] + neis[5] == sum)


	for h in hexagons:
		if h.type == 'flag':
			hexIs(h, 1)

		if h.type == 'inside':
			hexIs(h, 0)

		if h.type == '0':
			hexIs(h, 0)
			hexNeiSum(h, 0)

		if h.type == '1':
			hexIs(h, 0)
			hexNeiSum(h, 1)

		if h.type == '2':
			hexIs(h, 0)
			hexNeiSum(h, 2)

		if h.type == '3':
			hexIs(h, 0)
			hexNeiSum(h, 3)

		if h.type == '4':
			hexIs(h, 0)
			hexNeiSum(h, 4)


	if solver.check() == z3.unsat:
		print("Something's wrong, I can feel it")

	# Ok, there is a solution. Now lets see for which cell we can be sure about.
	ret = []
	for h in hexagons:
		if h.type != 'border': continue
		v = addVarIfMissing(h.r, h.q)
	
		solver.push()
		solver.add(v == 1)
		possibleBomb = solver.check() == z3.sat
		solver.pop()

		solver.push()
		solver.add(v == 0)
		possibleEmpty = solver.check() == z3.sat
		solver.pop()

		if possibleBomb and not possibleEmpty:
			ret.append((h, 1))

		if not possibleBomb and possibleEmpty:
			ret.append((h, 0))

		if possibleBomb and possibleEmpty:
			ret.append((h, 2))

		if not possibleBomb and not possibleEmpty:
			ret.append((h, None))


	# model = solver.model()
	# for h in hexagons:
	# 	if h.type != 'border': continue
	# 	v = addVarIfMissing(h.r, h.q)
	# 	ret.append((h, model[v]))

	return ret