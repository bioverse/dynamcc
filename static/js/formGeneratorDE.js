var copied = false;
var ran = false;

function copyFirstMutant(mutantEntriesValues, genotypeEntriesValues, numMutantsKey, numMutationsKey, typeMap)
{
	var numMutants = document.getElementById(numMutantsKey).value;

	if(copied)
	{
		if(!confirm("Are you sure you want to overwrite the data you already copied?"))
			return;
	}

	if(numMutants > 1)
	{
		for(var x = 2; x <= numMutants; x++)
		{
			for (var j = 0; j < mutantEntriesValues.length; j++)
			{
				if(mutantEntriesValues[j] != numMutationsKey)
				{
					var newKey = "Mutant"+x+"-" + mutantEntriesValues[j];
					var oneKey = "Mutant1-" + mutantEntriesValues[j];

					if(typeMap[mutantEntriesValues[j]] != "2")
					{
						document.getElementById(newKey).setAttribute("value",document.getElementById(oneKey).value);
					}
					else
					{
						var newSelectObj = document.getElementById(newKey);
						var oneSelectObj = document.getElementById(oneKey);

						for(var m = 0; m < oneSelectObj.options.length; m++)
						{
							if(oneSelectObj.options[m].selected == true)
								newSelectObj.options[m].setAttribute('selected',true);
						}
						document.getElementById(newKey).setAttribute("value",document.getElementById(oneKey).value);
					}
				}
			}
			//gene information is copied only if you've already specified the number of genes
			if(document.getElementById('Mutant' + x + '-' + genotypeEntriesValues[0] + '1') != null)
			{
				var mutations = document.getElementById('Mutant1-' + numMutationsKey).value;

				var newMutations = document.getElementById('Mutant' + x + '-' + numMutationsKey).value;

				if(newMutations < mutations)
					mutations = newMutations;

				for(var j = 1; j <= mutations; j++)
				{
					for(var k = 0; k < genotypeEntriesValues.length; k++)
					{
						var newKey = "Mutant"+x+"-" + genotypeEntriesValues[k] + j;
						var oneKey = "Mutant1-" + genotypeEntriesValues[k] + j;

						if(typeMap[genotypeEntriesValues[k]] != '2')
						{
							document.getElementById(newKey).setAttribute("value",document.getElementById(oneKey).value);
						}
						else
						{
							var newSelectObj = document.getElementById(newKey);
							var oneSelectObj = document.getElementById(oneKey);

							for(var m = 0; m < oneSelectObj.options.length; m++)
							{
								if(oneSelectObj.options[m].selected == true)
									newSelectObj.options[m].setAttribute('selected',true);
							}
							document.getElementById(newKey).setAttribute("value",document.getElementById(oneKey).value);
						}
					}
				}
			}
		}
		copied = true;
	}
}

function fillDefaultValues(paperTerms, mutantTerms, geneTerms, numMutantsKey, numMutationsKey,  typeMap, defaultMap)
{
	if(!ran)
	{
		console.log('I ran')
		ran = true;

		 for(var i = 0; i < paperTerms.length; i++)
		 {
			if(typeMap[paperTerms[i]] == '2')
			{
				var selectObj = document.getElementById(paperTerms[i])
				selectObj.options[0].setAttribute('selected',true);
				document.getElementById(paperTerms[i]).setAttribute('options', selectObj.options);
			}
			else
				document.getElementById(paperTerms[i]).setAttribute("value",defaultMap[paperTerms[i]]);
		}

		document.getElementById(numMutantsKey).setAttribute("onchange","");

		requestHTML('Mutant',0,'tabs',numMutantsKey,

			function(response)
			{
				setReadOnly(numMutantsKey);
				document.getElementById('tabs').innerHTML += response;
				document.getElementById('invisible-0').setAttribute('style', 'display:block;');
				document.getElementById('invisible').setAttribute('style', 'display:block;');
				document.getElementById('invisible-2').setAttribute('style', 'display:block;');
				$('#tabs').tabs()

				for(var i = 0; i < mutantTerms.length; i++)
				{
					if (typeMap[mutantTerms[i]] == '2')
					{
						var selectObj = document.getElementById("Mutant1-" + mutantTerms[i])
						selectObj.options[1].setAttribute('selected',true);
						document.getElementById("Mutant1-" + mutantTerms[i]).setAttribute('options', selectObj.options);
					}
					else
						document.getElementById("Mutant1-" + mutantTerms[i]).setAttribute("value",defaultMap[mutantTerms[i]]);
				}

				document.getElementById("Mutant1-" + numMutationsKey).setAttribute("onchange","");

				requestHTML('Gene',1,'tabs-1','Mutant1-' + numMutationsKey,

					function(response,index)
					{
						setReadOnly('Mutant1-' + numMutationsKey);
						divContainer = document.createElement('div');
						divContainer.innerHTML=response;
						document.getElementById('tabs-1').appendChild(divContainer);

						for(var j = 0; j < geneTerms.length; j++)
						{
							if (typeMap[geneTerms[j]] == '2')
							{
								var selectObj = document.getElementById("Mutant1-"+geneTerms[j]+"1");
								selectObj.options[0].setAttribute('selected',true);
								document.getElementById("Mutant1-"+geneTerms[j]+"1").setAttribute('options', selectObj.options);
							}
							else
								document.getElementById("Mutant1-"+geneTerms[j]+"1").setAttribute("value",defaultMap[geneTerms[j]]);
						}
					}
				);
			}
		);
	}
}

function checkDatabase(location)
{
	var http = new XMLHttpRequest();
	var url = "/query/";
	var params = "type=existence" + "&field=" + location + "&query=" + document.getElementById(location).value
	http.open("POST", url, true);

	//Send the proper header information along with the request
	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	http.onreadystatechange = function()
	{//Call a function when the state changes.
		if(http.readyState == 4 && http.status == 200)
		{
			var response = http.responseText;

			var outputNoun = '';

			if(location == 'DOI')
				outputNoun = 'DOI';
			if(location == 'Title')
				outputNoun = 'title';

			if(response == 'True')
			{
				alert('The database already contains a record with this exact ' + outputNoun + '. Please enter data from another paper.');
			}
			else
			{
				alert('The database does not contain a record with a matching ' + outputNoun + '.');
			}
		}
	}
	http.send(params);
}

function requestHTML(requestType, index, appendLocation, requestingElement, innerFunction)
{

	complete = false;

	var http = new XMLHttpRequest();
	var url = "/data_entry/";

	console.log(requestingElement)

	var params = "type=" + requestType + "&forms=" + document.getElementById(requestingElement).value + "&index=" + index;
	http.open("POST", url, true);

	//Send the proper header information along with the request
	http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

	http.onreadystatechange = function()
	{
		if(http.readyState == 4 && http.status == 200)
		{
			var response = http.responseText;

			innerFunction(response,index);
		}
	}
	http.send(params);
}

//key is the added value
function setAction(element,action)
{
	document.getElementById(element).setAttribute('action',action);
}
//change focus to target tab
function fixTab(targetTab)
{
	$( "#tabs" ).tabs("option","active",targetTab-1);
}

function setReadOnly(element)
{
	document.getElementById(element).setAttribute('readOnly',true);
}
