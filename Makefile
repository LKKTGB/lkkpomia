service ?= lkkpomia
env ?= testing

azure/deploy:
	git archive -o $(service).zip HEAD && \
	az webapp deployment source config-zip --resource-group $(service) --name $(service)-$(env) --src $(service).zip && \
	rm $(service).zip
azure/login:
	az login
azure/view:
	open https://$(service)-$(env).azurewebsites.net
