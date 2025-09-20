.PHONY: workspace

workspace:
		python make_workspace.py $(word 2,$(MAKECMDGOALS))

%:
		@: