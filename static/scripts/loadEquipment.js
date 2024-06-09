document.addEventListener('DOMContentLoaded', function(){
    var backgroundSelect = document.getElementById('background');
    var classSelect = document.getElementById('class');
    
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
                    addBackgroundEquipment(backgroundData.startingEquipment, 'background');
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
                var classData = data.class[0].startingEquipment.defaultData;
                if (classData) {
                    addClassEquipment(classData,'class');
                } else {
                    console.log('Clase no encontrada o no tiene equipamiento definido:', selectedClass);
                }
            })
            .catch(error => console.error('Error fetching class data:', error));
    }

    function fetchEquipmenCategorytData(itemConditions) {
        return fetch(`../../data/items-base.json`)
            .then(response => response.json())
            .then(data => {
                var equipmentData = data.baseitem;
                if (equipmentData) {
                    var filteredData = equipmentData.filter(item => evaluateConditions(item, itemConditions));
                    return filteredData;
                } else {
                    console.log('Item no encontrado:', itemConditions);
                    return [];
                }
            })
            .catch(error => {
                console.error('Error fetching class data:', error);
                return [];
            });
    }
    
    function evaluateConditions(item, conditions) {
        if (item.age) return false
        else {
        if (conditions.includes('weapon')) {
            if (!item.weapon) return false;
        }
        if (conditions.includes('Melee')) {
            if (item.type !== 'M') return false;
        }
        if (conditions.includes('instrumentMusical')) {
            if (item.type !== 'INS') return false;
        }
        if (conditions.includes('Martial')) {
            if (item.weaponCategory !== 'martial') return false;
        }
        if (conditions.includes('Simple')) {
            if (item.weaponCategory !== 'simple') return false;
        }
        if (conditions.includes('focusSpellcasting')) {
            if (item.type !== 'SCF') return false;
            if (conditions.includes('Arcane')) {
                if (item.scfType !== 'arcane') return false;
            } else if (conditions.includes('Druidic')) {
                if (item.scfType !== 'druid') return false;
            }
        }
        }

        return true;
    }
    function addClassEquipment(data, type) {
        const container = document.getElementById(`${type}Equipment`); // Asegúrate de tener un contenedor en tu HTML con este ID
        container.innerHTML = ''; // Limpia el contenedor antes de agregar nuevos elementos
    
        data.forEach((dataSet, index) => {
            const groupDiv = document.createElement('div');
            groupDiv.classList.add('checkbox-group');
    
            // Crear un nombre de grupo único para los radio buttons
            const groupName = `equipment-group-${index}`;
    
            // Iterar sobre todas las claves del objeto (a, b, c, etc.)
            Object.keys(dataSet).forEach(key => {
                dataSet[key].forEach(item => {
                    
                    const checkboxWrapper = document.createElement('div');
                    checkboxWrapper.classList.add('checkbox-wrapper');
    
                    const label = document.createElement('label');
                    let checkbox;
    
                    // Verificar si el item es un objeto o un string
                    if (typeof item === 'string') {
                        label.textContent = item;
                        checkbox = createRadioButton(groupName, item);
                        checkboxWrapper.appendChild(checkbox);
                        checkboxWrapper.appendChild(label);
                        groupDiv.appendChild(checkboxWrapper);
                    } else if (typeof item === 'object') {
                        if (item.item) {
                            label.textContent = `${item.item} (x${item.quantity})`;
                            checkbox = createRadioButton(groupName, item.item);
                            checkboxWrapper.appendChild(checkbox);
                            checkboxWrapper.appendChild(label);
                            groupDiv.appendChild(checkboxWrapper);
                        } else if (item.equipmentType) {
                            fetchEquipmenCategorytData(item.equipmentType)
                                .then(equipmentTypeList => {
                                    equipmentTypeList.forEach(equipmentItem => {
                                        const equipmentWrapper = document.createElement('div');
                                        equipmentWrapper.classList.add('checkbox-wrapper');
                                        
                                        const equipmentLabel = document.createElement('label');
                                        equipmentLabel.textContent = equipmentItem.name;
    
                                        const equipmentCheckbox = createRadioButton(groupName, equipmentItem.name);
                                        equipmentWrapper.appendChild(equipmentCheckbox);
                                        equipmentWrapper.appendChild(equipmentLabel);
                                        groupDiv.appendChild(equipmentWrapper);
                                    });
                                });
                        }
                    }
                });
            });
    
            // Añadir el grupo al contenedor principal
            container.appendChild(groupDiv);
        });
    }
    function createRadioButton(groupName, value) {
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = groupName;
        radio.value = value;
        return radio;
    }
    backgroundSelect.addEventListener('change', fetchBackgroundData);
    classSelect.addEventListener('change', fetchClassData);

    fetchBackgroundData(backgroundSelect);
    fetchClassData(classSelect);
});