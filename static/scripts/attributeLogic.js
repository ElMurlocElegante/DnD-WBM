document.addEventListener('DOMContentLoaded', function(){

    // Puntos iniciales disponibles
    let availablePoints = 27;


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
                    disableAllCheckbox();
                    if(raceData.ability){
                        enableCheckbox(raceData.ability, 'race');
                    } else {
                        enableAllCheckbox();
                    }

                } else {
                    console.log('Raza no encontrado:', selectedRace);
                }
            })
            .catch(error => console.error('Error fetching raza:', error));
    }


    function enableCheckbox(data, type) {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        var maxSkills = 0;
    
        // Eliminar todos los event listeners existentes
        raceBonusCheckboxes.forEach(function(checkbox) {
            checkbox.removeEventListener('change', checkboxChangeHandler);
        });
    
        Object.keys(data[0]).forEach(function(element) {
            if (element !== 'choose') {
                var checkbox = document.querySelector(`input[id="raceBonus-${element}${data[0][element]}"`);
                checkbox.disabled = true;
                checkbox.checked = true;
            } else if (element === 'choose') {
                // Obtener el recuento máximo de habilidades seleccionables
                maxSkills = data[0].choose.count;
    
                // Agregar event listener a cada checkbox
                data[0]['choose']['from'].forEach(function(attribute) {
                    var checkbox = document.querySelector(`input[id="raceBonus-${attribute}1"`);
                    checkbox.disabled = false;
                    checkbox.checked = false;
                    checkbox.addEventListener('change', function(event){
                        checkboxChangeHandler(maxSkills,event);
                    });
                });
            }
        });
        updateAllRowsTotalAndModifier();
    }
    
    // Actualizar el recuento máximo de habilidades
    function checkboxChangeHandler(maxSkills, event) {
        var checkedSkills = document.querySelectorAll('input[type="checkbox"][name="raceBonus"]:checked:not(:disabled)');
        if (checkedSkills.length > maxSkills) {
            event.target.checked = false;
        }
        updateAllRowsTotalAndModifier();
    }
    function enableAllCheckbox() {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        raceBonusCheckboxes.forEach(function(bonus) {
            bonus.disabled = false;
        })
        updateAllRowsTotalAndModifier();
        
    }
    function disableAllCheckbox() {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        raceBonusCheckboxes.forEach(function(bonus) {
            bonus.disabled = true;
            bonus.checked = false;
        })
    }
    // Función para actualizar los puntos disponibles
    function updateAvailablePoints() {
        const availablePointsInput = document.getElementById('availablePoints');
        availablePointsInput.value = availablePoints;
    }

    // Función para calcular el costo de aumento de un atributo
    function calculateCost(value) {
        // Valores de coste para aumentar cada atributo
        const costPerPoint = {
            8: 0,
            9: 1,
            10: 2,
            11: 3,
            12: 4,
            13: 5,
            14: 7,
            15: 9
        };
        return costPerPoint[value];
    }

    // Función para manejar cambios en los atributos
    function handleAttributeChange(input) {
        const currentValue = parseInt(input.value);
        const previousValue = parseInt(input.dataset.previousValue) || 8; // Valor predeterminado inicial
        const costDifference = calculateCost(currentValue) - calculateCost(previousValue);
        
        // Verificar si hay suficientes puntos disponibles para el cambio
        if (availablePoints - costDifference >= 0) {
            availablePoints -= costDifference;
            input.dataset.previousValue = currentValue; // Actualizar el valor anterior del input
        } else {
            // Restaurar el valor anterior si no hay suficientes puntos disponibles
            input.value = previousValue;
        }

        // Actualizar puntos disponibles
        updateAvailablePoints();

        // Actualizar total y modificador
        updateTotalAndModifier(input.closest('.attribute-row'));
    }
    function updateAllRowsTotalAndModifier() {
        const attributeRows = Array.from(document.querySelectorAll('.attribute-row')).filter(function(row) {
            return row.querySelector('label').getAttribute('for') !== 'availablePoints';
        });
        // Actualizar total y modificador inicialmente
        attributeRows.forEach(row => {
            updateTotalAndModifier(row);
        });
    }
    // Función para calcular el total y el modificador de un atributo
    function updateTotalAndModifier(row) {
        const baseValue = parseInt(row.querySelector('input[type="number"]').value);
        let raceBonus = 0;

        // Sumar bonificaciones de raza seleccionadas
        row.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            raceBonus += parseInt(checkbox.value);
        });

        // Calcular el total y el modificador
        const total = baseValue + raceBonus;
        const modifier = Math.floor((total - 10) / 2);

        // Actualizar los campos de total y modificador
        row.querySelector('input[name^="total"]').value = total;
        row.querySelector('input[name^="mod"]').value = modifier >= 0 ? `+${modifier}` : modifier;
    }

    // Agregar evento de escucha a los inputs de los atributos
    const attributeInputs = document.querySelectorAll('input[type="number"]');
    attributeInputs.forEach(input => {
        input.value = 8;
        input.addEventListener('input', () => handleAttributeChange(input));
    });

    var raceSelect = document.getElementById('race');
    raceSelect.addEventListener('change', fetchRaceData);
    fetchRaceData(raceSelect);

    // Agregar evento de escucha a los checkboxes de bonificación de raza
    const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
    raceBonusCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => updateTotalAndModifier(checkbox.closest('.attribute-row')));
    });

    // Actualizar puntos disponibles inicialmente
    updateAvailablePoints();
    updateAllRowsTotalAndModifier();

});