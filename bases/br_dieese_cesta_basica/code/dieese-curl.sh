#!/bin/sh

currentDate=`date +"%m%Y"`

# gasto_mensal 
curl -X POST https://www.dieese.org.br/cesta/produto \
	 -H "Content-Type: application/x-www-form-urlencoded" \
     -d "farinha=false&produtos=1&tipoDado=3&cidades=0&dataInicial=011959&dataFinal=${currentDate}" \
     -o "input/dieese-tempo-de-trabalho.html"

# tempo de trabalho 
curl -X POST https://www.dieese.org.br/cesta/produto \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "farinha=false&produtos=1&tipoDado=5&cidades=0&dataInicial=011959&dataFinal=${currentDate}" \
     -o "input/dieese-gasto-mensal.html"

