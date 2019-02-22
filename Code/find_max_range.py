from positions import positions

value1 = positions['extended'].values()
value2 = positions['seated'].values()

difference = [(a[0], abs((a[2] - a[1]))) for a in zip(positions['extended'].keys(), value1, value2)]
print difference
