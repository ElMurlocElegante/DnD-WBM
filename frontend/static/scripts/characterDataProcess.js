// async function updateCharacter(characterId, characterData) {
//     try {
//         const response = await fetch(`/api/characters/${characterId}`, {
//             method: 'PUT',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(characterData)
//         });

//         const result = await response.json();
//         if (response.ok) {
//             console.log('Character updated successfully:', result);
//         } else {
//             console.error('Failed to update character:', result.message);
//         }
//     } catch (error) {
//         console.error('Error updating character:', error);
//     }
// }
document.addEventListener('DOMContentLoaded', function() {
    const modalDelete = document.getElementById('modalDelete');
    const closeBtnDelete = document.querySelectorAll('.closeBtnDelete');
    const characterIdInput = document.getElementById('character_id');

    
    window.openModal = function(event, characterId) {
        event.preventDefault();
        characterIdInput.value = characterId;
        modalDelete.showModal();
    };

    
    closeBtnDelete.forEach(button => {
        button.addEventListener('click', () => {
            modalDelete.close();
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    function characterLevel(character) {
        const xp = parseInt(character.querySelector('[name="xp"]').innerText);
        // Definimos la tabla de experiencia y PB, no recuerdo si dijiste que habia json para esto, pero por si aca
        const experienceTable = {
            "experience": [
                {"xp": 0, "level": 1, "pb":2},
                {"xp": 300, "level": 2, "pb":2},
                {"xp": 900, "level": 3, "pb":2},
                {"xp": 2700, "level": 4, "pb":2},
                {"xp": 6500, "level": 5, "pb":3},
                {"xp": 14000, "level": 6, "pb":3},
                {"xp": 23000, "level": 7, "pb":3},
                {"xp": 34000, "level": 8, "pb":3},
                {"xp": 48000, "level": 9, "pb":4},
                {"xp": 64000, "level": 10, "pb":4},
                {"xp": 85000, "level": 11, "pb":4},
                {"xp": 100000, "level": 12, "pb":4},
                {"xp": 120000, "level": 13, "pb":5},
                {"xp": 140000, "level": 14, "pb":5},
                {"xp": 165000, "level": 15, "pb":5},
                {"xp": 195000, "level": 16, "pb":5},
                {"xp": 225000, "level": 17, "pb":6},
                {"xp": 265000, "level": 18, "pb":6},
                {"xp": 305000, "level": 19, "pb":6},
                {"xp": 355000, "level": 20, "pb":6}
            ]
        };
                
        // Iteramos sobre la tabla de experiencia en orden inverso para encontrar el nivel correcto, manejando con la tabla de exp puesta arriba
        for (let i = experienceTable.experience.length - 1; i >= 0; i--) {
            const xpThreshold = experienceTable.experience[i].xp;
            if (xp >= xpThreshold) {
                const levelValue = experienceTable.experience[i].level;
                const pb = experienceTable.experience[i].pb;
                const level = character.querySelector('[name="level"]');
                level.innerText = levelValue;
                pbInput = character.querySelector('[name="pb"]');
                pbInput.innerText = pb;
                break;
            }
        }
    }

    function alignmentFormat(character) {
        const alignment = character.querySelector('[name="alignment"]')
        alignment.innerText = ` ${alignment.innerText.match(/[A-Z]/g).join('')}`
    }
    const characters = document.querySelectorAll('.pc');
    characters.forEach(function(character) {
        characterLevel(character);
        alignmentFormat(character)
    });

});