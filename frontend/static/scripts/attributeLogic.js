document.addEventListener('DOMContentLoaded', function(){

    function fetchRaceData (event) {
        if (event.target === undefined){
            var selectedRace = event.value;
        } else {
            var selectedRace = event.target.value;
        }
        const [raceName, raceSource] = selectedRace.split('|');

        fetch('../../data/races.json')
            .then(response => response.json())
            .then(data => {
                const raceData = data.race.find(rc => rc.name === raceName && rc.source === raceSource);
                if (raceData) {
                    disableAllCheckbox();
                    if(raceData.ability){
                        enableCheckbox(raceData.ability, 'race');
                    } else {
                        enableAllCheckbox();
                    }

                } else {
                    console.log('Raza no encontrada:', selectedRace);
                }
            })
            .catch(error => console.error('Error fetching raza:', error));
    }

    function enableCheckbox(data, type) {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        let maxSelect = 0;
    
        // Eliminar todos los event listeners existentes
        raceBonusCheckboxes.forEach(checkbox => {
            checkbox.removeEventListener('change', checkboxChooseChangeHandler);
            checkbox.removeEventListener('change', checkboxAnyChangeHandler);
        });
    
        Object.keys(data[0]).forEach(element => {
            if (element !== 'choose') {
                const checkbox = document.querySelector(`input[id="raceBonus-${element}${data[0][element]}"`);
                checkbox.disabled = true;
                checkbox.checked = true;
            } else if (element === 'choose') {
                // Obtener el recuento máximo de habilidades seleccionables
                maxSelect = data[0].choose.count;
    
                // Agregar event listener a cada checkbox
                data[0].choose.from.forEach(attribute => {
                    const checkbox = document.querySelector(`input[id="raceBonus-${attribute}1"`);
                    checkbox.disabled = false;
                    checkbox.checked = false;
                    checkbox.addEventListener('change', event => {
                        checkboxChooseChangeHandler(maxSelect,event);
                    });
                });
            }
        });
        updateAllRowsTotalAndModifier();
    }

    function checkboxChooseChangeHandler(maxSelect, event) {
        var checkedBoxes = document.querySelectorAll('input[type="checkbox"][name="raceBonus"]:checked:not(:disabled)');
        if (checkedBoxes.length > maxSelect) {
            event.target.checked = false;
        }
        updateAllRowsTotalAndModifier();
    }

    function checkboxAnyChangeHandler(maxSelect, event) {
        var checkedBonus1 = document.querySelectorAll('input[type="checkbox"][name="raceBonus"][value="1"]:checked:not(:disabled)');
        var checkedBonus2 = document.querySelectorAll('input[type="checkbox"][name="raceBonus"][value="2"]:checked:not(:disabled)');

        // Verificar si hay más de una casilla de verificación seleccionada en la misma fila
        if (event.target.checked) {
            var rowDiv = event.target.parentElement.parentElement; // Obtener el div padre que contiene ambas casillas
            var checkboxesInRow = rowDiv.querySelectorAll('input[type="checkbox"][name="raceBonus"]:checked');
            
            if (checkboxesInRow.length > 1) {
                checkboxesInRow.forEach(function(cb) {
                    if (cb !== event.target) {
                        cb.checked = false; // Desmarcar la casilla de verificación que no fue seleccionada
                    }
                });
            }
        }
        if (checkedBonus1.length > maxSelect) {
            event.target.checked = false;
        }
        if (checkedBonus2.length > maxSelect || (event.target === checkedBonus1[0] && event.target.value === 1)) {
            event.target.checked = false;
        }
        
        updateAllRowsTotalAndModifier();
    }

    function enableAllCheckbox() {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        raceBonusCheckboxes.forEach(bonus => {
            bonus.removeEventListener('change', checkboxChooseChangeHandler);
            bonus.removeEventListener('change', checkboxAnyChangeHandler);
            bonus.disabled = false;
            bonus.addEventListener('change', event => {
                checkboxAnyChangeHandler(1,event);
            });
        })
        
        updateAllRowsTotalAndModifier();
        
    }
    function disableAllCheckbox() {
        const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
        raceBonusCheckboxes.forEach(bonus => {
            bonus.disabled = true;
            bonus.checked = false;
        })
    }

    // Función para actualizar los puntos disponibles
    function updateAvailablePoints(points) {
        const availablePointsInput = document.getElementById('availablePoints');
        availablePointsInput.value = points;
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

    // Función para actualizar los puntos de mejora de habilidad disponibles según el nivel del personaje
    function updateAvailableAbilityImprovements(level) {
        const availableAbilityImprovementsInput = document.getElementById('abilityScoreImprovementsInputs').querySelectorAll('input')
        const availableAbilityImprovementsPoints = document.getElementById('availableAbilityImprovements');
        const improvementsAtLevels = [4, 8, 12, 16, 19]; // Niveles donde se obtienen mejoras de habilidad
        const availableAbilityImprovements = improvementsAtLevels.filter(lvl => lvl <= level).length * 2; // Cada mejora permite aumentar dos puntos
        availableAbilityImprovementsPoints.value = availableAbilityImprovements;
        
        availableAbilityImprovementsInput.forEach(function(asi) {
            asi.value=0;
        })
        
    }

    // Función para calcular y actualizar los puntos de mejora de habilidad utilizados
    function updateASIValues() {
        const asiInputs = document.getElementById('abilityScoreImprovements').querySelectorAll('input[type="number"]');
        var totalASIUsed = 0;
        asiInputs.forEach(input => {
            totalASIUsed += parseInt(input.value) || 0;
        });

        const availableASI = parseInt(document.getElementById('availableAbilityImprovements').value);
        return availableASI - totalASIUsed;
    }

    // Función para manejar los cambios en los puntos de mejora de habilidad
    function handleASIChange(event) {
        const remainingASI = updateASIValues();
        if (remainingASI < 0) {
            event.target.value = parseInt(event.target.value) - 1;
        }
        const row = document.getElementById(`${event.target.name}Container`);
        updateTotalAndModifier(row);
    }
    // Evento para actualizar los puntos de mejora de habilidad cuando cambia el nivel del personaje
    ['change','input'].forEach(function(event) {
        document.getElementById('xp').addEventListener(event, function() {
            updateAvailableAbilityImprovements(parseInt(document.getElementById('level').value));
        });
    });


    // Inicializar puntos de mejora de habilidad basados en el nivel inicial del personaje
    updateAvailableAbilityImprovements(parseInt(document.getElementById('level').value));

    // Agregar evento de escucha a los inputs de ASI
    const ASIInputs = document.getElementById('abilityScoreImprovements').querySelectorAll('input[type="number"]');
    ASIInputs.forEach(input => {
        input.value = 0; // Valor inicial
        input.addEventListener('input', handleASIChange);
    });
    
    function handleAttributeChange(input) {
        var availablePoints = parseInt(document.getElementById('availablePoints').value)
        const currentValue = parseInt(input.value);
        const previousValue = parseInt(input.dataset.previousValue) || 8; // Valor predeterminado inicial
        const costDifference = calculateCost(currentValue) - calculateCost(previousValue);
        // Verificar si hay suficientes puntos disponibles para el cambio
        if ((availablePoints - costDifference) >= 0) {
            availablePoints -= costDifference; 
            input.dataset.previousValue = currentValue; // Actualizar el valor anterior del input
        } else {
            // Restaurar el valor anterior si no hay suficientes puntos disponibles
            input.value = previousValue;
        }
        // Actualizar puntos disponibles
        updateAvailablePoints(availablePoints);

        // Actualizar total y modificador
        updateTotalAndModifier(input.closest('.attribute-row'));
    }

    function updateAllRowsTotalAndModifier() {
        const attributeRows = Array.from(document.getElementById('attributes').querySelectorAll('.attribute-row')).filter(row => row.querySelector('label').getAttribute('for') !== 'availablePoints');
        // Actualizar total y modificador inicialmente
        attributeRows.forEach(row => {
            updateTotalAndModifier(row);
        });
    }

    // Función para calcular el total y el modificador de un atributo
    function updateTotalAndModifier(row) {
        const baseInput = row.querySelector('input[type="number"]')
        const baseValue = parseInt(baseInput.value);
        const ASIValue = parseInt(document.getElementById('abilityScoreImprovementsInputs').querySelector(`input[name="${baseInput.name}"]`).value)
        let raceBonus = 0;

        // Sumar bonificaciones de raza seleccionadas
        row.querySelectorAll('input[type="checkbox"]:checked').forEach(checkbox => {
            raceBonus += parseInt(checkbox.value);
        });

        // Calcular el total y el modificador
        const total = baseValue + raceBonus + ASIValue;
        const modifier = Math.floor((total - 10) / 2);

        // Actualizar los campos de total y modificador
        row.querySelector('input[name^="total"]').value = total;
        row.querySelector('input[name^="mod"]').value = modifier >= 0 ? `+${modifier}` : modifier;
    }
    // Actualizar puntos disponibles inicialmente
    updateAvailablePoints(27);
    // Agregar evento de escucha a los inputs de los atributos
    const attributeInputs = document.getElementById('attributes').querySelectorAll('.attribute-row input[type="number"]');
    attributeInputs.forEach(input => {
        input.value = 8;
        input.min = 8; // Establecer el valor mínimo desde JavaScript
        handleAttributeChange(input);
        input.addEventListener('input', () => handleAttributeChange(input));
    });

    const raceSelect = document.getElementById('race');
    raceSelect.addEventListener('change', fetchRaceData);
    fetchRaceData(raceSelect);

    // Agregar evento de escucha a los checkboxes de bonificación de raza
    const raceBonusCheckboxes = document.querySelectorAll('input[name="raceBonus"]');
    raceBonusCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => updateTotalAndModifier(checkbox.closest('.attribute-row')));
    });

    updateAllRowsTotalAndModifier();

});
