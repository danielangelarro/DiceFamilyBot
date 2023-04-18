PYTHON=python3
FILENAME=bot.py
.DEFAULT_GOAL=run

run:
	${PYTHON} ${FILENAME}
	echo 'Bot init...'