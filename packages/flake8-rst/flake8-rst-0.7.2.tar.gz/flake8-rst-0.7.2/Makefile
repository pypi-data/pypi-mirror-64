
.PHONY: clean
clean:
	-rm -rf build dist webim.egg-info htmlcov .eggs

minor:
	bumpversion minor

major:
	bumpversion major

patch:
	bumpversion patch

publish:
	pip install wheel twine
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

upload: clean publish
