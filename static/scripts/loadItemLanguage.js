document.addEventListener('DOMContentLoaded', function(){

    function fetchBackgroundData (event) {
        
        if (event.target === undefined){
            var selectedBackground = event.value;
        } else  {
            var selectedBackground = event.target.value
        }
        fetch('../../data/backgrounds.json')
            .then(response => response.json())
            .then(data => {
                var backgroundData = data.background.find(function(bg) {
                    return bg.name === selectedBackground;
                });

                if (backgroundData) {
                    // Verificar si existe una copia
                    if (backgroundData._copy) {
                        // Reemplazar backgroundData con los datos de la copia
                        var copyData = data.background.find(function (bg) {
                            return bg.name === backgroundData._copy.name && bg.source === backgroundData._copy.source;
                        });
                        if (copyData) {
                            backgroundData = copyData;
                        }
                    }
                    const proficienciesEntries = Object.entries(backgroundData).filter(function(entry) {
                        const key = entry[0];
                        return key.includes('Proficiencies') && !key.includes('skillProficiencies');
                    });
                    if (proficienciesEntries){
                        addProficiencies(proficienciesEntries, 'background');
                    }
                } else {
                    console.log('Background no encontrado:', selectedBackground);
                }
            })
            .catch(error => console.error('Error fetching backgrounds:', error));
    }

    function fetchClassData (event) {
        if (event.target === undefined){
            var selectedClass = event.value;
        } else  {
            var selectedClass = event.target.value
        }
        
        fetch(`../../data/class/class-${selectedClass.toLowerCase()}.json`)
            .then(response => response.json())
            .then(data => {
                var classData = data.class[0].startingProficiencies
                if (classData) {
                    const proficienciesEntries = Object.entries(classData).filter(function(entry) {
                        const key = entry[0];
                        return !key.includes('skills');
                    });
                    if (proficienciesEntries) {
                        addProficiencies(proficienciesEntries, 'race');
                    }
                } else {
                    console.log('Clase no encontrada o no tiene habilidades definidas:', selectedClass);
                }
            })
            .catch(error => console.error('Error fetching class data:', error));
    }

    function fetchRaceData (event) {
        if (event.target === undefined){
            var selectedRace = event.value;
        } else {
            var selectedRace = event.target.value;
        }
        var [raceName, raceSource] = selectedRace.split('|');

        fetch('../../data/races.json')
            .then(response => response.json())
            .then(data => {
                var raceData = data.race.find(function(rc) {
                    return rc.name === raceName && rc.source === raceSource;
                });
                if (raceData) {
                    const proficienciesEntries = Object.entries(raceData).filter(function(entry) {
                        const key = entry[0];
                        return key.includes('Proficiencies') && !key.includes('skillProficiencies');
                    });
                        if (proficienciesEntries) {
                            addProficiencies(proficienciesEntries, 'race');
                        }
                } else {
                    console.log('Raza no encontrado:', selectedRace);
                }
            })
            .catch(error => console.error('Error fetching raza:', error));
    }
    function createCheckbox(element, type) {
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.name = `${element.toLowerCase()}-${type}`;
        checkbox.id = `${element.toLowerCase()}-${type}`;
        checkbox.value = `${element.toLowerCase()}`;
        // checkbox.addEventListener('change', checkProficiencies);

        var label = document.createElement('label');
        label.htmlFor = `${element.toLowerCase()}-${type}`;
        label.textContent = `${element}`;

        var container = document.createElement('div');
        container.className = 'checkbox-container';
        container.appendChild(checkbox);
        container.appendChild(label);

        return container;
    }
    function addProficiencies(data, type) {
        console.log(type, data);
        data.forEach(function(element) {
            element.forEach(function(proficiency) {
                console.log(proficiency);
                createCheckbox(proficiency, type)
            });

        });
    }
    const languages = document.getElementById('languageProfList');
    const items = document.getElementById('itemProfList');

    const selectedBackground = document.getElementById('background');
    const selectedClass = document.getElementById('class');
    const selectedRace = document.getElementById('race');
    
    selectedBackground.addEventListener('change', fetchBackgroundData);
    selectedClass.addEventListener('change', fetchClassData);
    selectedRace.addEventListener('change', fetchRaceData);
    fetchBackgroundData(selectedBackground);
    fetchClassData(selectedClass);
    fetchRaceData(selectedRace);
    
});