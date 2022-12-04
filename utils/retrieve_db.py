def retrieve_db(i):
	with open(f"db/db{str(i)}.txt", "r") as f:
		content = f.read()
		f.close()
	if not content:
		raise Exception("File read failed")
	arr = content.split('-')
	return arr