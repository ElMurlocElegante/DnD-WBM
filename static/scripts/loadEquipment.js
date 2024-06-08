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

    function addClassEquipment(data,type) {
        const container = document.getElementById(`${type}Equipment`); // Asegúrate de tener un contenedor en tu HTML con este ID
        container.innerHTML = ''; // Limpia el contenedor antes de agregar nuevos elementos
    
        data.forEach((dataSet, index) => {
            console.log(dataSet, index )
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
                    } else if (typeof item === 'object') {
                        if (item.item) {
                            label.textContent = `${item.item} (x${item.quantity})`;
                            checkbox = createRadioButton(groupName, item.item);
                        } else if (item.equipmentType) {
                            label.textContent = item.equipmentType;
                            checkbox = createRadioButton(groupName, item.equipmentType);
                        }
                    }
    
                    // Añadir el checkbox y el label al wrapper y luego al grupo
                    checkboxWrapper.appendChild(checkbox);
                    checkboxWrapper.appendChild(label);
                    groupDiv.appendChild(checkboxWrapper);
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