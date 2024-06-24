#It's breakfast time, we don't have any fruit at home, we need to go to supermarket, but we need a organized list

#solution

const fruitsArray = ['maçãs', 'bananas', 'laranjas', 'morangos', 'kiwis'];

function fruitsList(fruit) {
  return `- ${fruit} (2 unidades)`;
}

#using the  .map() method to create a market buy list based on fruits array

const newArrayOfStrings = fruitsArray.map(fruitsList);

console.log('Lista de Compras de Frutas:');
console.log(newArrayOfStrings.join('\n'));


"""

result:

Lista de Compras de Frutas:
- maçãs (2 unidades)
- bananas (2 unidades)
- laranjas (2 unidades)
- morangos (2 unidades)
- kiwis (2 unidades)

"""



