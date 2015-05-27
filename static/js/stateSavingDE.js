function enableBeforeUnload() {
    window.onbeforeunload = function (e) {
        return "Discard changes?";
    };
}
function disableBeforeUnload() {
    window.onbeforeunload = null;
}

function loadState()
{
	console.log(localStorage["SavedState"])
	if(localStorage["SavedState"] == 'true')
	{
		localStorage["SavedState"] = false;
		var mutants = parseInt(localStorage[numMutantsKey]);
		ran = false;
		document.getElementById(numMutantsKey).setAttribute("value",mutants);
		generateMutantForms("tabs");
		
		//so you can refresh the page again without getting trapped by recordState
		
		
		for(var i = 0; i < mainEntriesValues.length; i++)
			document.getElementById(mainEntriesValues[i]).setAttribute("value",localStorage[mainEntriesValues[i]]);
			
		for(var j = 1; j <= mutants; j++)
		{
			for(var i = 0; i < mutantEntriesValues.length; i++)
			{
				var key = "Mutant"+j+ "-" + mutantEntriesValues[i];
				document.getElementById(key).setAttribute("value",localStorage[key]);
			}
				
			var numMutations = parseInt(localStorage["Mutant"+j+ "-" + numMutationsKey]);
			
			generateMutationEntryForms(j);
		
			for(var i = 1; i <= numMutations; i++)
			{
				for(var k = 0; k < genotypeEntriesValues.length; k++)
				{
					var key = "Mutant"+j+ "-" + genotypeEntriesValues[k] + i;
					
					if(genotypeEntriesValues[k] == 'Gene Mutation')
						key += "x";
						
					document.getElementById(key).setAttribute("value",localStorage[key]);
					//localStorage["Native-Mutant"+j+ "-" + genotypeEntries[k] + i] = '';
				}
			}
		}
	}
	else
	{
		localStorage.clear();
		//document.getElementById("tabs").setAttribute("innerHTML","<ul id = \"tab-inner\" class=\"tabs\"></ul>");
		//console.log(document.getElementById("tabs").innerHTML);
	}
}


function recordState()
{
	localStorage["SavedState"] = true;
	
	for(var i = 0; i < mainEntriesValues.length; i++)
		localStorage[mainEntriesValues[i]] = document.getElementById(mainEntriesValues[i]).value;
	
	var numMutants = document.getElementById(numMutantsKey).value;
	
	for(var j = 1; j <= numMutants; j++)
	{
		for(var i = 0; i < mutantEntriesValues.length; i++)
			localStorage["Mutant"+j+ "-" + mutantEntriesValues[i]] = document.getElementById("Mutant"+j+ "-" + mutantEntriesValues[i]).value;
			
		var numMutations = document.getElementById("Mutant"+j+ "-" + numMutationsKey).value;
		
		for(var i = 1; i <= numMutations; i++)
		{
			for(k = 0; k < genotypeEntriesValues.length; k++)
			{
				var key = "Mutant"+j+ "-" + genotypeEntriesValues[k] + i;
				
				localStorage[key] = document.getElementById(key).value;
			}
		}
	}

}
