# Cave à Vin

## Présentation
```
La cave à vin contient six bouteilles, les données (temperatures, humidités) sont récupérées à l'aide d'un capteur DHT22. 
Lors de l'ajout d'une bouteille dans la cave, une LED s'allume afin d'indiquer la présence d'une bouteille sur l'emplacement. 

```

## Raspberry
```
La raspberry est branché sur le système d'alimentation de la cave à vin. Lorsque la raspberry démarre, il va exécuter les deux 
programmes python (qui récupère les données et qui permettent le contrôles des LEDs), ajouté dans le fichier /etc/rc.local, 
qui s'exécute au démmarage de la raspberry. 

```
